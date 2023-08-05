# -*- coding: utf-8 -*-

class APIError(Exception):
    def __init__(self, errno, msg):
        self.errno = errno
        self.msg = msg

    def __str__(self):
        return '%s (%s)' % (self.msg, self.errno)
