import ply.lex as lex
import logging


class InstatLexer(object):
    # List of token names
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
    t_STRING    = r'\"([^"]|\n)*\"'
    t_HASHTAG   = r'\#[a-zA-Z0-9_][a-zA-Z0-9_]*'
    t_LPAREN    = r'\('
    t_RPAREN    = r'\)'
    t_LBRACK    = r'\{'
    t_RBRACK    = r'\}'
    t_LBRACE    = r'\['
    t_RBRACE    = r'\]'
    t_EQUALS    = r'='
    t_PLUS      = r'\+'
    t_MINUS     = r'\-'
    t_SEMICOLON = r';'
    t_COLON     = r':'
    t_MULTIPLY  = r'\*'
    t_DIVIDE    = r'/'
    t_EQUIV     = r'(==)'
    t_NONEQUIV  = r'(!=)'
    t_RELOP     = r'(<=)|(>=)|(<)|(>)'
    t_COMMA     = r'(,)'

    # A regular expression rule with some action code

    def t_DATE(self, t):
        r'[0-3]?[0-9]/[01]?[0-9]/[0-9]+[ ][01]?[0-9]:[0-5][0-9][ ]((AM)|(PM))'
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = InstatLexer.reserved.get(t.value, 'ID')    # Check for reserved words
        if t.type == 'NONE':
            t.value = None
        if t.type == 'TRUE':
            t.value = True
            t.type = 'BOOLEAN'
        if t.type == 'FALSE':
            t.value = False
            t.type = 'BOOLEAN'
        return t

    def t_USER(self, t):
        r'\@[a-zA-Z0-9_][a-zA-Z0-9_\.]*[a-zA-Z0-9_]'
        return t

    def t_LOCATION(self, t):
        r'\@\((\d+\.\d+), ?(\d+\.\d+)\)'
        return t

    def t_FLOAT(self, t):
        r'\d+\.\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print "Float value too large", t.value
            t.value = 0.0
        return t

    def t_INTEGER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print "Integer value too large", t.value
            t.value = 0
        return t

    def t_COMMENT(self, t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        pass


    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.type = "NEWLINE"
        if t.lexer.paren_count == 0:
            return t

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    def __init__(self):
        # Set up a logging object
        logging.basicConfig(
            level = logging.DEBUG,
            filename = "parselog.txt",
            filemode = "w",
            format = "%(filename)10s:%(lineno)4d:%(message)s"
        )
        log = logging.getLogger()
        # Build the lexer
        self.lexer = lex.lex(module=self, debug=True, debuglog=log)

    def test(self, data):
        self.lexer.input(data)
        token_list = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print tok
            token_list.append(tok)
        return token_list