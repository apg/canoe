import ply.yacc as yacc

from lex import tokens
from ast import ConfigNode, AssNode, DeclNode, WatchNode, ValueNode, DerefNode

    
def p_config(p):
    """config : top_assignments watch_blocks
    """
    print "Config"
    p[0] = ConfigNode(top_assignments=p[1], watches=p[2])

def p_top_assignments(p):
    """top_assignments : top_assignment top_assignments
                       |
    """
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_watch_blocks(p):
    """watch_blocks : watch_block watch_blocks
                    |
    """
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_watch_block(p):
    """watch_block : WATCH STRING LCURLY filter_declarations \
                     route_declaration RCURLY
                     
    """
    p[0] = WatchNode(p[2], p[4], p[5])

def p_top_assignment(p):
    """top_assignment : IDENTIFIER EQUALS declaration
    """
    p[0] = AssNode(identifier=p[1], value=p[3])

def p_declaration(p):
    """declaration : filter_declaration
                   | route_declaration
    """
    p[0] = p[1]

def p_filter_declarations(p):
    """filter_declarations : filter_declaration filter_declarations
                           |
    """
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_filter_declaration(p):
    """filter_declaration : FILTER path LCURLY assignments RCURLY
                          | FILTER dereference
    """
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = DeclNode('filter', p[2], p[4])

def p_route_declaration(p):
    """route_declaration : ROUTE path LCURLY assignments RCURLY
                         | ROUTE dereference
    """
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = DeclNode('route', p[2], p[4])

def p_assignments(p):
    """assignments : assignment COMMA assignments
                   | assignment
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_assignment(p):
    """assignment : IDENTIFIER EQUALS value
    """
    p[0] = AssNode(p[1], p[3])

def p_path(p):
    """path : IDENTIFIER
            | IMPORT_PATH
    """
    p[0] = str(p[1])

def p_value(p):
    """value : NUMBER 
             | STRING
             | BOOL
             | dereference
    """
    possible_values = {
        'false': False,
        'False': False,
        'true': True,
        'True': True,
        }
    p[0] = ValueNode(possible_values.get(p[1], p[1]))

def p_dereference(p):
    """dereference : AT IDENTIFIER
    """
    p[0] = DerefNode(p[2])

def p_error(p):
    raise SyntaxError("Syntax Error! on line %d" % p.lexer.lineno)


parser = yacc.yacc()

