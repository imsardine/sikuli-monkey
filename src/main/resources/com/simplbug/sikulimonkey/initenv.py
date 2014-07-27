def _init():
    import sys, os, pickle, time

    # appending PYTHONPATH from environment variables
    if os.environ.has_key('PYTHONPATH'):
        for entry in os.environ['PYTHONPATH'].split(os.pathsep):
            if entry != '': sys.path.insert(0, entry)
    print "Init MonkeyRunner/Sikuli Env. PYTHONPATH = %s" % sys.path

    # retreving params passed from Robot Framework (Python)
    args = {}
    if 'MONKEYRUNNER_PARAMS' in os.environ:
        args = pickle.load(open(os.environ['MONKEYRUNNER_PARAMS'], 'rb'))
        print 'MONKEYRUNNER_PARAMS:', args

    # global functions
    from andwalker import get_default_serialno
    from com.simplbug.sikulimonkey import AndroidScreen
    serialno = get_default_serialno()
    scr = AndroidScreen(serialno)
    robot = scr.getRobot()
    device = robot.getDevice()

    dict = globals()
    dict['sleep'] = time.sleep
    dict['exit'] = sys.exit
    dict['SCREEN'] = scr
    dict['device'] = device
    dict['capture'] = scr.capture
    dict['exists'] = scr.exists
    dict['find'] = scr.find
    dict['findAll'] = scr.findAll
    dict['wait'] = scr.wait
    dict['waitVanish'] = scr.waitVanish
    dict['tap'] = scr.tap
    dict['click'] = scr.tap
    dict['longPress'] = scr.longPress
    dict['pan'] = scr.pan
    dict['dragDrop'] = scr.pan # alias
    dict['type'] = scr.type
    dict['pressHome'] = robot.pressHome
    dict['pressMenu'] = robot.pressMenu
    dict['pressBack'] = robot.pressBack
    dict['pressSearch'] = robot.pressSearch
    dict['pressBackspace'] = robot.pressBackspace
    dict['pressEnter'] = robot.pressEnter
    dict['pressDpadUp'] = robot.pressDpadUp
    dict['pressDpadDown'] = robot.pressDpadDown
    dict['pressDpadLeft'] = robot.pressDpadLeft
    dict['pressDpadRight'] = robot.pressDpadRight
    dict['pressDpadCenter'] = robot.pressDpadCenter
    #dict['flick'] = scr.flick

    dict['ARGS'] = args
    dict['DEVICE_SERIAL_NUMBER'] = serialno
    dict['DEVICE_MODEL'] = device.getProperty('build.model')
    dict['DEVICE_RESOLUTION'] = (int(device.getProperty('display.width')), int(device.getProperty('display.height')))
    dict['DEVICE_PLATFORM_VERSION'] = device.getProperty('build.version.release')
    dict['DEVICE_API_LEVEL'] = int(device.getProperty('build.version.sdk'))

    # set bundle path. sys.argv[0] always returns full path of the script.
    import sys, os.path as path
    from org.sikuli.script import Settings
    Settings.BundlePath = path.normpath(path.dirname(sys.argv[0]))

_init()
from org.sikuli.script import Settings
from org.sikuli.script import Pattern
from org.sikuli.script import FindFailed
from org.sikuli.script.natives import Vision
Settings.WaitScanRate = 0.25
Vision.setParameter('MinTargetSize', 24)
Settings.DebugLogs = True
