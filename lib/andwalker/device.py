import logging, re, os.path as path, subprocess, time
from exceptions import ShellError
from utils import get_default_serialno

_logger = logging.getLogger(__name__)

class Device(object):

    def __init__(self, serialno=None):
        self._serialno = serialno

    @property
    def serialno(self):
        return self._serialno

    @property
    def model(self):
        raise NotImplementedError()

    @property
    def platform_version(self):
        raise NotImplementedError()

    @property
    def api_level(self):
        raise NotImplementedError()

    @property
    def resolution(self):
        raise NotImplementedError()

    def file_exists(self, pathname):
        try:
            self.shell('ls %s' % pathname)
            return True
        except ShellError, e:
            if e.errmsg.endswith('No such file or directory'): return False
            raise

    def shell(self, cmd):
        stdout = self._shell_exec(cmd + '; echo $?')
        _logger.debug("The RAW output, including trailing exit status, of ADB shell command [%s] is [[[%s]]]", cmd, stdout)
        stdout = stdout.rstrip().replace('\r\r\n', '\r\n').replace('\r\n', '\n')

        stdout, retcode = stdout.rsplit('\n', 1)
        retcode = int(retcode)
        if retcode != 0:
            errmsg = 'failed to execute ADB shell command (%i)\n%s' % (retcode, stdout)
            raise ShellError(retcode, errmsg)
        return stdout

    def _shell_exec(self, cmd):
        raise NotImplementedError()

    @property
    def current_activity_package(self):
        # MonkeyDevice.getProperty('am.current.package') doesn't work in the beginning.
        return self.current_activity_component.split('/') [0]

    @property
    def current_activity_component(self):
        # mFocusedActivity: HistoryRecord{40a571d8 com.android.vending/com.google.android.finsky.activities.MainActivity}
        act_dump = self.shell('dumpsys activity')
        match = re.search(r'mFocusedActivity:.* (?P<component>[\w./]+)}', act_dump)
        if not match: raise Exception("fail to parse current activity; the output of 'dumpsys activity' is [[[%s]]]" % act_dump)
        return match.group('component')

    def is_package_installed(self, package):
        return package in self.installed_packages

    @property
    def installed_packages(self):
        output = self.shell('pm list packages')
        return [match.group(1) for match in re.finditer('^package:(.*)$', output, re.MULTILINE)]

    def uninstall_package(self, package):
        if package not in self.installed_packages: return
        self.shell('pm uninstall %s' % package)
        assert package not in self.installed_packages

    def open_app(self, package, activity=None):
        if activity:
           component = '%s/%s' % (package, activity) 
           self.shell('am start -n %s' % component)
        else:
           self.shell('am start -a android.intent.action.MAIN -c android.intent.category.LAUNCHER %s' % package)

    def clear_app(self, package):
        self.shell('pm clear %s' % package)

class ADBDevice(Device):

    def __init__(self, serialno=None):
        if serialno is None: serialno = get_default_serialno()
        super(ADBDevice, self).__init__(serialno)

    def _shell_exec(self, cmd):
        cmd = ['adb', '-s', self._serialno, 'shell' , cmd]
        return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

class MonkeyDevice(Device):

    def __init__(self, serialno, monkey_device):
        super(MonkeyDevice, self).__init__(serialno)
        self._monkey_device = monkey_device
        self._model = None
        self._resolution = None

    @property
    def model(self):
        if self._model: return self._model

        self._model = self._monkey_device.getProperty('build.model')
        return self._model

    @property
    def platform_version(self):
        return self._monkey_device.getProperty('build.version.release')

    @property
    def api_level(self):
        return int(self._monkey_device.getProperty('build.version.sdk'))

    @property
    def resolution(self):
        if self._resolution: return self._resolution

        device = self._monkey_device
        x = int(device.getProperty('display.width'))
        y = int(device.getProperty('display.height'))
        self._resolution = x, y
        return self._resolution

    @property
    def current_activity_package(self):
        # MonkeyDevice.getProperty('am.current.package') doesn't work in the beginning.
        return self.current_activity_component.split('/') [0]

    @property
    def current_activity_component(self):
        # mFocusedActivity: HistoryRecord{40a571d8 com.android.vending/com.google.android.finsky.activities.MainActivity}
        act_dump = self.shell('dumpsys activity')
        match = re.search(r'mFocusedActivity:.* (?P<component>[\w./]+)}', act_dump)
        if not match: raise Exception("fail to parse current activity; the output of 'dumpsys activity' is [[[%s]]]" % act_dump)
        return match.group('component')

    def is_package_installed(self, package):
        return package in self.installed_packages

    @property
    def installed_packages(self):
        output = self.shell('pm list packages')
        return [match.group(1) for match in re.finditer('^package:(.*)$', output, re.MULTILINE)]

    def uninstall_package(self, package):
        if package not in self.installed_packages: return
        self.shell('pm uninstall %s' % package)
        assert package not in self.installed_packages

    def _abs_path(self, rel_path):
        base = path.dirname(__file__)
        return path.join(base, rel_path)

    def _shell_exec(self, cmd):
        return self._monkey_device.shell(cmd)

class MonkeySikuliDevice(MonkeyDevice):

    def __init__(self, serialno, sikuli_screen):
        super(MonkeySikuliDevice, self).__init__(serialno, sikuli_screen.getRobot().getDevice())
        self._screen = sikuli_screen

    def install_package(self, package):
        if package in self.installed_packages: return

        screen = self._screen
        self._monkey_device.startActivity(action='android.intent.action.VIEW', data='market://details?id=%s' % package)

        screen.tap(self._abs_path('googleplay_install.png'))
        screen.tap(self._abs_path('googleplay_accept_download.png'))

        # return when the package is completely installed
        timeout = time.time() + 2 * 60
        while time.time() < timeout:
            if package in self.installed_packages: return
            time.sleep(5)
        raise Exception("The package [%s] is not successfully installed within timeout (2 min)" % package)
