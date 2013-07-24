def echo(line, buffer):
    print line


class PrefixedEcho(object):
    
    def __init__(self, prefix=''):
        self._prefix = prefix

    def __call__(self, line, buffer):
        print '%s%s' % (self._prefix, line)
