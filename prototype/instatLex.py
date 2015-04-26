import ply.lex as lex
import sys
import re

# List of token names.   This is always required
reserved = {
	'main': 'MAIN',
    'print': 'PRINT',
    'show': 'SHOW',
    'search': 'SEARCH',
    'set': 'SET',
    'string': 'STRINGF',
    'length': 'LENGTH',
    'login': 'LOGIN',
    'logout': 'LOGOUT',
    'barchart': 'BARCHART',
    'piechart': 'PIECHART',
    'from': 'FROM',
    'to': 'TO',
    'if': 'IF',
    'else': 'ELSE',
    'elif': 'ELIF',
    'while': 'WHILE',
    'for': 'FOR',
    'in': 'IN',
    'function': 'FUNCTION',
    'True': 'TRUE',
    'False': 'FALSE',
    'None': 'NONE',
    'or' : 'OR',
    'and' : 'AND',
    'not' : 'NOT',
    }

tokens = [
	'INTEGER',
    'FLOAT',
    'BOOLEAN',
    'USER',
    'LOCATION',
    'HASHTAG',
    'LPAREN',
    'RPAREN',
    'RBRACK',
    'LBRACK',
    'RBRACE',
    'LBRACE',
    'EQUALS',
    'PLUS',
    'MINUS',
    'ID',
    'SEMICOLON',
    'COLON',
    'DATE',
    'MULTIPLY',
    'DIVIDE',
    'EQUIV',
    'NONEQUIV',
    'RELOP',
    'INDENT',
    'DEDENT',
    'WS',
    'NEWLINE',
    'COMMA',
    'STRING',
] + list(reserved.values())

# Regular expression rules for simple tokens
t_STRING 	= r'\"([^"]|\n)*\"'
t_HASHTAG 	= r'\#[a-zA-Z0-9_][a-zA-Z0-9_]*'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACK    = r'\{'
t_RBRACK    = r'\}'
t_LBRACE    = r'\['
t_RBRACE    = r'\]'
t_EQUALS    = r'='
t_PLUS      = r'\+'
t_MINUS 	= r'\-'
t_SEMICOLON = r';'
t_COLON     = r':'
t_MULTIPLY  = r'\*'
t_DIVIDE    = r'/'
t_EQUIV     = r'(==)'
t_NONEQUIV  = r'(!=)'
t_RELOP     = r'(<=)|(>=)|(<)|(>)'
t_COMMA     = r'(,)'

# A regular expression rule with some action code

def t_DATE(t):
    r'[0-3]?[0-9]/[01]?[0-9]/[0-9]+[ ][01]?[0-9]:[0-5][0-9][ ]((AM)|(PM))'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    if t.type == 'NONE':
        t.value = None
    if t.type == 'TRUE':
        t.value = True
        t.type = 'BOOLEAN'
    if t.type == 'FALSE':
        t.value = False
        t.type = 'BOOLEAN'
    return t

def t_USER(t):
    r'\@[a-zA-Z0-9_][a-zA-Z0-9_\.]*[a-zA-Z0-9_]'
    return t

def t_LOCATION(t):
    r'\@\((\d+\.\d+), ?(\d+\.\d+)\)'
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    return t

def t_INTEGER(t):
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


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    if t.lexer.paren_count == 0:
        return t

# Whitespace
def t_WS(t):
    r' [ ]+ '
    if t.lexer.at_line_start and t.lexer.paren_count == 0:
        return t


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# the following methods: track_tokens_filter(), _new_token(), DEDENT(), INDENT(), indentation_filter(), filter(), and instatLexer() are from:
# http://www.dalkescientific.com/writings/diary/GardenSnake.py
# 
# Python's syntax has three INDENT states
#  0) no colon hence no need to indent
#  1) "if 1: go()" - simple statements have a COLON but no need for an indent
#  2) "if 1:\n  go()" - complex statements have a COLON NEWLINE and must indent
NO_INDENT = 0
MAY_INDENT = 1
MUST_INDENT = 2

# only care about whitespace at the start of a line
def track_tokens_filter(lexer, tokens):
    lexer.at_line_start = at_line_start = True
    indent = NO_INDENT
    saw_colon = False
    for token in tokens:
        token.at_line_start = at_line_start

        if token.type == "COLON":
            at_line_start = False
            indent = MAY_INDENT
            token.must_indent = False
            
        elif token.type == "NEWLINE":
            at_line_start = True
            if indent == MAY_INDENT:
                indent = MUST_INDENT
            token.must_indent = False

        elif token.type == "WS":
            assert token.at_line_start == True
            at_line_start = True
            token.must_indent = False

        else:
            # A real token; only indent after COLON NEWLINE
            if indent == MUST_INDENT:
                token.must_indent = True
            else:
                token.must_indent = False
            at_line_start = False
            indent = NO_INDENT

        yield token
        lexer.at_line_start = at_line_start

def _new_token(type, lineno):
    tok = lex.LexToken()
    tok.type = type
    tok.value = None
    tok.lineno = lineno
    return tok

# Synthesize a DEDENT tag
def DEDENT(lineno):
    return _new_token("DEDENT", lineno)

# Synthesize an INDENT tag
def INDENT(lineno):
    return _new_token("INDENT", lineno)

# Track the indentation level and emit the right INDENT / DEDENT events.
def indentation_filter(tokens):
    # A stack of indentation levels; will never pop item 0
    levels = [0]
    token = None
    depth = 0
    prev_was_ws = False
    for token in tokens:
        yield token
    
# The top-level filter adds an ENDMARKER, if requested.
# Python's grammar uses it.
def filter(lexer, add_endmarker = False):
    token = None
    tokens = iter(lexer.token, None)
    tokens = track_tokens_filter(lexer, tokens)
    for token in indentation_filter(tokens):
        yield token


class instatLexer(object):
    def __init__(self, debug=0, optimize=0, lextab='lextab', reflags=0):
        self.lexer = lex.lex(debug=debug, optimize=optimize, lextab=lextab, reflags=reflags)
        self.token_stream = None
    def input(self, s, add_endmarker=False):
        self.lexer.paren_count = 0
        self.lexer.input(s)
        self.token_stream = filter(self.lexer, add_endmarker)
    def token(self):
        try:
            return self.token_stream.next()
        except StopIteration:
            return None


# Put CODE HERE TO TEST LEXER
if __name__ == '__main__':

    # Build the lexer
    lexer = instatLexer()
    # code
    #this doesnt work RGGGGGG
    data = """
"""

    # Give the lexer some input
    lexer.input(data)

    # Check tokens
    while True:
        tok = lexer.token()
        if not tok: break      # No more input
        elif not hasattr(tok, 'line') and not hasattr(tok, 'lexpos'):
            print tok.type
        else: print tok
