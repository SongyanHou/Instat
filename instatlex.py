import ply.lex as lex
import logging


class InstatLexer(object):
    reserved = {
        'print': 'PRINT',
        'show': 'SHOW',
        'search': 'SEARCH',
        'string': 'STRINGF',
        'from': 'FROM',
        'to': 'TO',
        'if': 'IF',
        'else': 'ELSE',
        'elif': 'ELIF',
        'while': 'WHILE',
        'for': 'FOR',
        'in': 'IN',
        'length': 'LENGTH',
        'function': 'FUNCTION',
        'barchart': 'BARCHART',
        'piechart': 'PIECHART',
        'login': 'LOGIN',
        'logout': 'LOGOUT',
        'main': 'MAIN',
        'set': 'SET'
    }

    unreserved_tokens = [
        'NONE',
        'INTEGER',
        'FLOAT',
        'BOOLEAN',
        'STRING',
        'HASHTAG',
        'ID',
        'SEMICOLON',
        'NEWLINE',
        'USER',
        'LOCATION',
        'DATE'
    ]

    tokens = unreserved_tokens + list(reserved.values())

    # Tokens
    t_STRING = r'\"([^"]|\n)*\"'
    t_HASHTAG = r'\#[a-zA-Z0-9_][a-zA-Z0-9_]*'
    t_SEMICOLON = r';'
    t_FROM = r'from'
    t_TO = r'to'
    t_LOGIN = r'login'
    t_LOGOUT = r'logout'
    t_FOR = r'for'
    t_WHILE = r'while'
    t_IF = r'if'
    t_ELSE = r'else'
    t_ELIF = r'elif'
    t_IN = r'in'
    t_LENGTH = r'length'
    t_FUNCTION = r'function'
    t_PIECHART = r'piechart'
    t_BARCHART = r'barchart'
    t_MAIN = r'main'
    t_SHOW = r'show'
    t_SEARCH = r'search'
    t_PRINT = r'print'
    t_SET = r'set'

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

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        t.type = InstatLexer.reserved.get(t.value, 'ID')    # Check for reserved words
        return t

    def t_DATE(self, t):
        r'[0-3]?[0-9]/[01]?[0-9]/[0-9]+[ ][01]?[0-9]:[0-5][0-9][ ]((AM)|(PM))'
        return t

    def t_USER(selt, t):
        r'\@[a-zA-Z0-9_][a-zA-Z0-9_\.]*[a-zA-Z0-9_]'
        t.value = t.value[1:]
        return t

    def t_LOCATION(self, t):
        r'\@\('
        t.value = None
        return t

    def t_NONE(self, t):
        r'None'
        t.value = None
        return t

    def t_INTEGER(self, t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print "Integer value too large", t.value
            t.value = 0
        return t

    def t_FLOAT(self, t):
        r'\d+\.\d+'
        try:
            t.value = float(t.value)
        except ValueError:
            print "Float value too large", t.value
        return t

    def t_BOOLEAN(self, t):
        r'True|False'
        if t.value == 'True':
            t.value = True
        else:
            t.value = False
        return t

    def t_COMMENT(self, t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        pass

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        t.type = 'NEWLINE'

    t_ignore = ' \t'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

if __name__ == '__main__':
    instatlexer = InstatLexer()

    data = '''
        // Hello world program for Instat 

        if else elif main from login logout for while in piechart barchart
        to
        function
        set
        length

        @asd.asdasdasd
        @(
        search
        25/08/2015 10:50 AM

        print "hello world";
        show #helloworld;
        '''

    instatlexer.lexer.input(data)

    while True:
        tok = instatlexer.lexer.token()
        if not tok:
            break
        else:
            print tok