# this file generates the token for primitive type int, float, boolean and string
# built-in function string is implemented

tokens = (
    'INTEGER',
    'PRINT',
    'STRING',
    'FLOAT',
    'BOOLEAN',
    'STRINGF',
    )

# Tokens

t_PRINT = r'print'
t_STRINGF = r'string'

def t_STRING(t):
    r'\"([^"]|\n)*\"'
    t.value = t.value
    return t

def t_BOOLEAN(t):
    r'True|False'
    if(t.value == 'True'):
        t.value = True
    else:
        t.value = False
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print "Float value too large", t.value
    return t

def t_INTEGER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print "Integer value too large", t.value
        t.value = 0
    return t

t_ignore = " \t"

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

def p_statement_assign(p):
    'statement : PRINT expression'
    print p[2]

def p_statement_string_function_int(p):
    'expression : STRINGF INTEGER'
    p[0] = '"' + str(p[2]) + '"'

def p_statement_string_function_float(p):
    'expression : STRINGF FLOAT'
    p[0] = '"' + str(p[2]) + '"'

def p_statement_string_function(p):
    'expression : STRINGF BOOLEAN'
    p[0] = '"' + str(p[2]) + '"'

def p_expression_integer(p):
    "expression : INTEGER"
    p[0] = p[1]

def p_expression_float(p):
    "expression : FLOAT"
    p[0] = p[1]

def p_expression_boolean(p):
    "expression : BOOLEAN"
    p[0] = p[1]

def p_expression_string(p):
    "expression : STRING"
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
