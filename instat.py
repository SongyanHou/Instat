from show import show
import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

reserved = {
    'print': 'PRINT',
    'show': 'SHOW'
}

tokens = ['NUMBER', 'STRING', 'HASHTAG', 'ID', 'SEMICOLON', 'NEWLINE'] + list(reserved.values())

# Tokens

t_STRING = r'\"([^"]|\n)*\"'
t_HASHTAG = r'\#[a-zA-Z0-9_][a-zA-Z0-9_]*'
t_SEMICOLON = r';'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Integer value too large", t.value
        t.value = 0
    return t


def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = 'NEWLINE'

t_ignore = r' \t'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex(debug=True, debuglog=log)

# Parsing rules

def p_program(p):
    '''program : program statement
               | statement'''
    pass


def p_statement_print(p):
    'statement : PRINT string end'
    print_string = p[2]
    print print_string[1:-1]


def p_statement_show(p):
    'statement : SHOW hashtag end'
    tag_name = p[2]
    show(tag_name[1:])


def p_string(p):
    'string : STRING'
    p[0] = p[1]


def p_hashtag(p):
    'hashtag : HASHTAG'
    p[0] = p[1]


def p_end(p):
    'end : SEMICOLON'
    p[0] = None


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc(debug=True, debuglog=log)

data = '''
// Hello world program for Instat
print "hello world";
show #helloworld;
'''

yacc.parse(data, debug=log)