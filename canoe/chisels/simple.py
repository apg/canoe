import re


class RegexpFilter(object):
    
    def __init__(self, regex=None, invert=False):
        self._invert = invert
        if not regex:
            raise ValueError("regex argument can't be blank")
        print "COMPILING!", regex
        self._re = re.compile(regex)
        print "init regexp filter", regex
        
    def __call__(self, line, buffer):
        print "TEST: ", line, self._re.search(line)
        found = bool(self._re.search(line))
        if found and (not self._invert):
            print "           just lets go have one last look"
            return (line, buffer)
        elif self._invert:
            print "           found due to invert!"
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

