from parser import parser
from lex import lexer

DEFAULTS = {
    'EXTRA_LOAD_PATH': '',
}

class Config(object):

    def __init__(self, watches, properties=None):
        self.watching = watches
        self._properties = DEFAULTS.copy()
        self._properties.update(properties or {})

    @classmethod
    def from_file(cls, file):
        config = None
        env = DEFAULTS.copy()
        with open(file) as f:
            inp = f.read()
            cn = parser.parse(inp, lexer=lexer)
            config = cn.evaluate(env)
        return config
