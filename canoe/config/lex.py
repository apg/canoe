import ply.lex as lex

reserved_words = {
    'route': 'ROUTE',
    'watch': 'WATCH',
    'filter': 'FILTER',
}

tokens = [
    'COMMA',
    'EQUALS',
    'AT',
    'LCURLY',
    'RCURLY',
    'NUMBER',
    'STRING',
    'BOOL',
    'IMPORT_PATH',
    'IDENTIFIER',
] + reserved_words.values()

t_AT = r'@'
t_EQUALS = r'='
t_COMMA = r','
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_ignore_COMMENT = r'\#.*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_STRING(t):
    r'"(\\[nrt"\\]|[^\\\"])*"'
    replacements = [
        ('\\n', '\n'),
        ('\\r', '\r'),
        ('\\t', '\t'),
        ('\\"', '"'),
        ('\\\\', '\\'),
        ]
    for s, r in replacements:
        t.value = t.value.replace(s, r)
    t.value = t.value[1:-1]
    return t

def t_IMPORT_PATH(t):
    r'"[a-zA-Z_][a-zA-Z0-9_](\.[a-zA-Z_][a-zA-Z0-9_])*"'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() == 'true':
        t.type = 'BOOL'
        t.value = True
    elif t.value.lower() == 'false':
        t.type = 'BOOL'
        t.value = False
    else:
        t.type = reserved_words.get(t.value, 'IDENTIFIER')
    return t
    
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print "Illegal character '%s' on line %d, position %d." % \
        (t.value[0], t.lexer.lineno, t.lexer.lexpos)
    raise SystemExit()

# Build the lexer
lexer = lex.lex()
