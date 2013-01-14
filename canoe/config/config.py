from parser import parser
from lex import lexer

class Config(object):

    def __init__(self, watches):
        self.watching = watches

    @classmethod
    def from_file(cls, file):
        with open(file) as f:
            inp = f.read()
            cn = parser.parse(inp, lexer=lexer)

            print cn
            env = {}
            config = cn.evaluate(env)
            print env
            return config
