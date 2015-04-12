import unittest
import instatlex


class TestInstatLexer(unittest.TestCase):
    def setUp(self):
        self.lexer = instatlex.InstatLexer()

    def test_print(self):
        data = '''
        print
        '''
        tokens = self.lexer.test(data)
        self.assertEqual(len(tokens), 1, 'incorrect number of tokens')
        self.assertEqual(tokens[0].type, 'PRINT', 'first token not PRINT')
        self.assertEqual(tokens[0].value, 'print', 'value of token not print')

    def test_primitivetypes(self):
        pass

    def test_ignorecomments(self):
        pass

    def test_ignorewhitespace(self):
        pass

    def test_newline(self):
        pass

    def test_errors(self):
        pass


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestInstatLexer)
    unittest.TextTestRunner(verbosity=2).run(suite)