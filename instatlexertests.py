import unittest
import instat_test


class TestInstatLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = instat_test.InstatLexer()

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

    def test_from_to(self):
        data = '''
        from 25/08/2015 10:50 AM to 20/11/2015 10:50 AM
        from to
        FROM TO
        from1 to2
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 10, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'FROM', 'token not FROM')
        self.assertEqual(tokens[1].type, 'DATE', 'token not DATE')
        self.assertEqual(tokens[1].value, '25/08/2015 10:50 AM', 'value not correct')
        self.assertEqual(tokens[2].type, 'TO', 'token not TO')
        self.assertEqual(tokens[3].type, 'DATE', 'token not DATE')
        self.assertEqual(tokens[3].value, '20/11/2015 10:50 AM', 'value not correct')
        self.assertEqual(tokens[4].type, 'FROM', 'token not FROM')
        self.assertEqual(tokens[5].type, 'TO', 'token not TO')
        self.assertNotEqual(tokens[6].type, 'FROM', 'token is FROM')
        self.assertNotEqual(tokens[7].type, 'TO', 'token is TO')
        self.assertNotEqual(tokens[6].type, 'FROM', 'token is FROM')
        self.assertNotEqual(tokens[7].type, 'TO', 'token is TO')


    def test_if_else_elif(self):
        data = '''
        if else elif
        If Else Elif
        if1 else2 elif3
        if()
        {}
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 14, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'IF', 'token not IF')
        self.assertEqual(tokens[1].type, 'ELSE', 'token not ELSE')
        self.assertEqual(tokens[2].type, 'ELIF', 'token not ELIF')
        self.assertNotEqual(tokens[3].type, 'IF', 'token is IF')
        self.assertNotEqual(tokens[4].type, 'ELSE', 'token is ELSE')
        self.assertNotEqual(tokens[5].type, 'ELIF', 'token is ELIF')
        self.assertNotEqual(tokens[6].type, 'IF', 'token is IF')
        self.assertNotEqual(tokens[7].type, 'ELSE', 'token is ELSE')
        self.assertNotEqual(tokens[8].type, 'ELIF', 'token is ELIF')
        self.assertEqual(tokens[9].type, 'IF', 'token not IF')
        self.assertEqual(tokens[10].type, 'LPAREN', 'token is t_LPAREN')
        self.assertEqual(tokens[11].type, 'RPAREN', 'token is t_RPAREN')
        self.assertEqual(tokens[12].type, 'LBRACK', 'token is t_LPAREN')
        self.assertEqual(tokens[13].type, 'RBRACK', 'token is t_RPAREN')

    def test_while(self):
        data = '''
        while
        While
        while222
        while()
        {}
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 8, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'WHILE', 'token not WHILE')
        self.assertNotEqual(tokens[1].type, 'WHILE', 'token is WHILE')
        self.assertNotEqual(tokens[2].type, 'WHILE', 'token is WHILE')
        self.assertEqual(tokens[3].type, 'WHILE', 'token not WHILE')
        self.assertEqual(tokens[4].type, 'LPAREN', 'token is LPAREN')
        self.assertEqual(tokens[5].type, 'RPAREN', 'token is RPAREN')
        self.assertEqual(tokens[6].type, 'LBRACK', 'token is LPAREN')
        self.assertEqual(tokens[7].type, 'RBRACK', 'token is RPAREN')

    def test_for(self):
        data = '''
        for
        For
        for11
        for(a in b)
        {}
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 11, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'FOR', 'token not FOR')
        self.assertNotEqual(tokens[1].type, 'FOR', 'token is FOR')
        self.assertNotEqual(tokens[2].type, 'FOR', 'token is FOR')
        self.assertEqual(tokens[3].type, 'FOR', 'token not FOR')
        self.assertEqual(tokens[4].type, 'LPAREN', 'token is t_LPAREN')
        self.assertEqual(tokens[5].type, 'ID', 'token is ID')
        self.assertEqual(tokens[6].type, 'IN', 'token is IN')
        self.assertEqual(tokens[7].type, 'ID', 'token is ID')
        self.assertEqual(tokens[8].type, 'RPAREN', 'token is RPAREN')
        self.assertEqual(tokens[9].type, 'LBRACK', 'token is LPAREN')
        self.assertEqual(tokens[10].type, 'RBRACK', 'token is RPAREN')

    def test_in(self):
        data = '''
        in
        In
        int
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'IN', 'token not IN')
        self.assertNotEqual(tokens[1].type, 'IN', 'token is IN')
        self.assertNotEqual(tokens[2].type, 'IN', 'token is IN')

    def test_length(self):
        data = '''
        length
        Length
        lengthfor
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'LENGTH', 'token not LENGTH')
        self.assertNotEqual(tokens[1].type, 'LENGTH', 'token is LENGTH')
        self.assertNotEqual(tokens[2].type, 'LENGTH', 'token is LENGTH')

    def test_function(self):
        data = '''
        function
        Function
        function111
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'FUNCTION', 'token not FUNCTION')
        self.assertNotEqual(tokens[1].type, 'FUNCTION', 'token is FUNCTION')
        self.assertNotEqual(tokens[2].type, 'FUNCTION', 'token is FUNCTION')

    def test_barchart(self):
        data = '''
        barchart
        Barchart
        barchartfor
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'BARCHART', 'token not BARCHART')
        self.assertNotEqual(tokens[1].type, 'BARCHART', 'token is BARCHART')
        self.assertNotEqual(tokens[2].type, 'BARCHART', 'token is BARCHART')

    def test_piechart(self):
        data = '''
        piechart
        Piechart
        piechartfor
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'PIECHART', 'token not PIECHART')
        self.assertNotEqual(tokens[1].type, 'PIECHART', 'token is PIECHART')
        self.assertNotEqual(tokens[2].type, 'PIECHART', 'token is PIECHART')

    def test_login(self):
        data = '''
        login
        Login
        loginme
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'LOGIN', 'token not LOGIN')
        self.assertNotEqual(tokens[1].type, 'LOGIN', 'token is LOGIN')
        self.assertNotEqual(tokens[2].type, 'LOGIN', 'token is LOGIN')

    def test_logout(self):
        data = '''
        logout
        Logout
        logoutme
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'LOGOUT', 'token not LOGOUT')
        self.assertNotEqual(tokens[1].type, 'LOGOUT', 'token is LOGOUT')
        self.assertNotEqual(tokens[2].type, 'LOGOUT', 'token is LOGOUT')

    def test_main(self):
        data = '''
        main
        Main
        main2
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'MAIN', 'token not MAIN')
        self.assertNotEqual(tokens[1].type, 'MAIN', 'token is MAIN')
        self.assertNotEqual(tokens[2].type, 'MAIN', 'token is MAIN')

    def test_main(self):
        data = '''
        set
        Set
        set2
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 3, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'SET', 'token not SET')
        self.assertNotEqual(tokens[1].type, 'SET', 'token is SET')
        self.assertNotEqual(tokens[2].type, 'SET', 'token is SET')



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
