import subprocess, re, logging

_logger = logging.getLogger(__name__)

_ATTACHED_DEVICES_BEGIN = 'List of devices attached'

def get_serialnos():
    cmd = ['adb', 'devices']
    raw = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].replace('\r\n', '\n')
    _logger.debug("RAW output of 'adb devices' [[[%s]]]" % raw)
    begin = raw.index(_ATTACHED_DEVICES_BEGIN) + len(_ATTACHED_DEVICES_BEGIN)
    raw = raw[begin:].strip()

    return [match.group(1) for match in re.finditer('^(.+?)\s+', raw, re.MULTILINE)]

def get_default_serialno():
    nos = get_serialnos()
    if len(nos) == 0: raise RuntimeError('There is no connected device.')
    return nos[0]
