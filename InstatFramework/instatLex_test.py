import ply.lex as lex
import sys
import re

# List of token names.   This is always required
reserved = {
	'number' : 'TNUMBER',
	}
tokens = [
	'EQUALS',
] + list(reserved.values())

t_EQUALS    = r'='

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID') #looks in reserved list, if can't find, assigns it to type ID 
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.type = "NEWLINE"
    if t.lexer.paren_count == 0:
        return t
        
def _new_token(type, lineno):
    tok = lex.LexToken()
    tok.type = type
    tok.value = None
    tok.lineno = lineno
    return tok

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

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
    a = 32
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