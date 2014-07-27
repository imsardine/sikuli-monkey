class ShellError(Exception):

    def __init__(self, errno, errmsg):
        self.errno = errno
        self.errmsg = errmsg
        super(ShellError, self).__init__(*(errno, errmsg))
