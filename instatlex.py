import ply.lex as lex
import logging


class InstatLexer(object):
    reserved = {
        'print': 'PRINT',
        'show': 'SHOW',
        'search': 'SEARCH',
        'string': 'STRINGF'
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
        'NEWLINE'
    ]

    tokens = unreserved_tokens + list(reserved.values())

    # Tokens
    t_STRING = r'\"([^"]|\n)*\"'
    t_HASHTAG = r'\#[a-zA-Z0-9_][a-zA-Z0-9_]*'
    t_SEMICOLON = r';'

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

    def t_FLOAT(t):
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

    t_ignore = r' \t'

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

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

if __name__ == '__main__':
    lexer = InstatLexer()
    data = '''
        print
        '''
    lexer.test(data)