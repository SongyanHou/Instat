import unittest
import instatlex


class TestInstatLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = instatlex.InstatLexer()

    def test_print(self):
        data = '''
        print "hello world";
        Print
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 4, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'PRINT', 'first token not PRINT')
        self.assertEqual(tokens[0].value, 'print', 'value of token not print')
        self.assertEqual(tokens[1].type, 'STRING', 'second token not STRING')
        self.assertEqual(tokens[1].value, '"hello world"', 'value of token not "hello world"')
        self.assertEqual(tokens[2].type, 'SEMICOLON', 'third token not SEMICOLON')
        self.assertEqual(tokens[2].value, ';', 'value of token not ;')
        self.assertNotEqual(tokens[3].type, 'PRINT', 'token is PRINT')

    def test_show(self):
        data = '''
        show #helloworld;
        Show
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 4, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'SHOW', 'first token not SHOW')
        self.assertEqual(tokens[0].value, 'show', 'value of token not show')
        self.assertEqual(tokens[1].type, 'HASHTAG', 'second token not HASHTAG')
        self.assertEqual(tokens[1].value, '#helloworld', 'value of token not #helloworld')
        self.assertEqual(tokens[2].type, 'SEMICOLON', 'third token not SEMICOLON')
        self.assertEqual(tokens[2].value, ';', 'value of token not ;')
        self.assertNotEqual(tokens[3].type, 'SHOW', 'token is SHOW')

    def test_search(self):
        data = '''
        search
        Search
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 2, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'SEARCH', 'token not SEARCH')
        self.assertEqual(tokens[0].value, 'search', 'value of token not search')
        self.assertNotEqual(tokens[1].type, 'SEARCH', 'token is SEARCH')

    def test_stringf(self):
        data = '''
        string
        STRING
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 2, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'STRINGF', 'token not STRINGF')
        self.assertEqual(tokens[0].value, 'string', 'value of token not string')
        self.assertNotEqual(tokens[1].type, 'STRINGF', 'token is STRINGF')

    def test_integer(self):
        data = '''
        10
        100.0
        int
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'INTEGER', 'token not INTEGER')
        self.assertNotEqual(tokens[1].type, 'INTEGER', 'token is INTEGER')
        self.assertNotEqual(tokens[2].type, 'INTEGER', 'token is INTEGER')

    def test_float(self):
        data = '''
        10.0
        100
        float
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'FLOAT', 'token not FLOAT')
        self.assertNotEqual(tokens[1].type, 'FLOAT', 'token is FLOAT')
        self.assertNotEqual(tokens[2].type, 'FLOAT', 'token is FLOAT')

    def test_boolean(self):
        data = '''
        True
        False
        true
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'BOOLEAN', 'token not BOOLEAN')
        self.assertEqual(tokens[0].value, True, 'token value not True')
        self.assertEqual(tokens[1].type, 'BOOLEAN', 'token not BOOLEAN')
        self.assertEqual(tokens[1].value, False, 'token value not False')
        self.assertNotEqual(tokens[2].type, 'BOOLEAN', 'token is BOOLEAN')

    def test_none(self):
        data = '''
        None1
        None
        none
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertNotEqual(tokens[0].type, 'NONE', 'token is NONE')
        self.assertEqual(tokens[1].type, 'NONE', 'token not NONE')
        self.assertEqual(tokens[1].value, None, 'token value not None')
        self.assertNotEqual(tokens[2].type, 'NONE', 'token is NONE')

    def test_string(self):
        data = '''
        "string"
        string
        STRING
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'STRING', 'token not STRING')
        self.assertEqual(tokens[0].value, '"string"', 'value of token not "string"')
        self.assertNotEqual(tokens[1].type, 'STRING', 'token is STRING')
        self.assertNotEqual(tokens[2].type, 'STRING', 'token is STRING')

    #def test_ignorecomments(self):
        #pass

    #def test_ignorewhitespace(self):
        #pass

    #def test_newline(self):
        #pass

    #def test_errors(self):
        #pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInstatLexer)
    unittest.TextTestRunner(verbosity=2).run(suite)