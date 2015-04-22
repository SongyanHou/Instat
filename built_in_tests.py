import unittest
import instat_built_in
import chart_function


class TestBuiltIn(unittest.TestCase):
    def test_show(self):
        pass

    def test_search(self):
        pass

    def test_print(self):
        pass

    def test_length(self):
        pass

    def test_string(self):
        pass

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBuiltIn)
    unittest.TextTestRunner(verbosity=2).run(suite)