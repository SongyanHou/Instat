__author__ = 'Jane'

import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

reserved = {
    'print': 'PRINT',
    'show': 'SHOW'
}

tokens = ['STRING', 'HASHTAG', 'ID'] + list(reserved.values())

literals = [';']

# Tokens

t_STRING = r'\"([^"]|\n)*\"'
t_HASHTAG = r'\#[a-zA-Z0-9_][a-zA-Z0-9_]*'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass

t_ignore = r' \t\n'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Test it out
#data = '''
#// Hello world program for Instat
#print "hello world";
#show #helloworld;
#'''

# Give the lexer some input
#lexer.input(data)

# Tokenize
#while True:
#    tok = lexer.token()
#    if not tok:
#        break      # No more input
#    print tok


def p_print_stmt(p):
    'print_stmt : PRINT STRING ;'
    print p[2]


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
yacc.yacc()

while 1:
    try:
        s = raw_input('input > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)