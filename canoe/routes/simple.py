
class EchoRoute(object):
    
    def __init__(self, prefix=None):
        self._prefix = prefix or ''
    
    def __call__(self, line, buffer):
        print "%s%s" % (self._prefix, line)
