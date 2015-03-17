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

t_ignore = r'\s'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lex.lex()