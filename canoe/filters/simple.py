import re

# TODO: shouldn't be the case that chisels are always classes

class PassThroughFilter(object):

    def __call__(self, line, buffer):
        return (line, buffer)


class RegexpFilter(object):
    
    def __init__(self, regex=None, invert=False):
        self._invert = invert
        if not regex:
            raise ValueError("regex argument can't be blank")
        self._re = re.compile(regex)
        
    def __call__(self, line, buffer):
        found = bool(self._re.search(line))
        if found and (not self._invert):
            return (line, buffer)
        elif self._invert:
            return (line, buffer)
        else:
            return (None, None)

        
class WordsFilter(RegexpFilter):
    
    def __init__(self, words, invert=False):
        regex = ''
        if not hasattr(words, '__iter__'):
            esc = map(re.escape, words)
            regex = '\b(%s)\b' % '|'.join(esc)
        else:
            regex = re.escape(words)
        RegexpFilter.__init__(self, regex, invert)

