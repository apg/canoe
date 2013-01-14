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
    print "Top assignments"
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_watch_blocks(p):
    """watch_blocks : watch_block watch_blocks
                    |
    """
    print "Watch blocks"
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_watch_block(p):
    """watch_block : WATCH STRING LCURLY chisel_declarations \
                     route_declaration RCURLY
                     
    """
    print "Watch block"
    print "chisels", p[4]
    p[0] = WatchNode(p[2], p[4], p[5])

def p_top_assignment(p):
    """top_assignment : IDENTIFIER EQUALS declaration
    """
    print "Top assignment"
    p[0] = AssNode(identifier=p[1], value=p[3])

def p_declaration(p):
    """declaration : chisel_declaration
                   | route_declaration
    """
    print "Declaration"
    p[0] = p[1]

def p_chisel_declarations(p):
    """chisel_declarations : chisel_declaration chisel_declarations
                           |
    """
    print "Chisel declarations"
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_chisel_declaration(p):
    """chisel_declaration : CHISEL path LCURLY assignments RCURLY
    """
    print "Chisel declaration"
    p[0] = DeclNode('chisel', p[2], p[4])

def p_route_declaration(p):
    """route_declaration : ROUTE path LCURLY assignments RCURLY
    """
    print "Route declaration"
    p[0] = DeclNode('route', p[2], p[4])

def p_assignments(p):
    """assignments : assignment COMMA assignments
                   | assignment
    """
    print "Assignments"
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_assignment(p):
    """assignment : IDENTIFIER EQUALS value
    """
    print "Assignment"
    p[0] = AssNode(p[1], p[3])

def p_path(p):
    """path : IDENTIFIER
            | IMPORT_PATH
    """
    print "path", p[1]
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
    # TODO: Need to handle dereference
    p[0] = ValueNode(possible_values.get(p[1], p[1]))

def p_dereference(p):
    """dereference : AT IDENTIFIER
    """
    print "Dereference"
    p[0] = DerefNode(p[2])

def p_error(p):
    print repr(p)
    raise SyntaxError("Syntax Error!")


parser = yacc.yacc()

