import re


class WordsFilter(object):
    
    def __init__(self, words, invert=False):
        if not hasattr(words, '__iter__'):
            esc = map(re.escape, words)
            self._re = re.compile('(%s)' % '|'.join(esc))
        else:
            self._re = re.compile(words)
        self._invert = invert

    def __call__(self, line, buffer):
        found = bool(self._re.search(line))
        if found == self._invert:
            return (line, buffer)
        else:
            return (None, None)


class RegexpFilter(object):
    
    def __init__(self, re, invert=False):
        self._invert = invert
        self._re = re.compile(re)
        
