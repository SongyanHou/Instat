# -----------------------------------------------------------------------------
# calc.py
#
# A simple calculator with variables.   This is from O'Reilly's
# "Lex and Yacc", p. 63.
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0,"../..")

tokens = (
    'NUMBER',
    'PRINT',
    'STRING',
    )

# Tokens

t_PRINT = r'PRINT'
#def t_PRINT(t):
#    r'print'
#    print "go into print"

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Integer value too large", t.value
        t.value = 0
    return t

t_ignore = " \t"

t_STRING = r'\"[a-zA-Z0-9_][a-zA-Z0-9_]*\"'

#def t_STRING(t):
#    r'[a-z_][a-z0-9_]*'
#    try:
#        t.value = 10
#        print "string"
#    except ValueError:
#        print "Failed to read "
#        t.value = 10;
#    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

# Parsing rules

# dictionary of names

def p_print_statement(p):
    "statement : PRINT  expression "
    print "go int print statement"
    print p[2]

def p_expression_group(p):
    "expression : '(' expression ')'"
    print "go into p_expression_group expression"
    p[0] = p[2]

def p_expression_number(p):
    "expression : NUMBER"
    print "go into NUMBER expression"
    p[0] = p[1]

def p_expression_string(p):
    "expression : STRING"
    print "go into STRING expression"
    p[0] = p[1]


def p_error(p):
    print "Syntax error at '%s'" % p.value

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    yacc.parse(s)