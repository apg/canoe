
class EchoRoute(object):
    
    def __call__(self, line, buffer):
        print line
