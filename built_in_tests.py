import unittest
import instat_built_in as instat


class TestBuiltIn(unittest.TestCase):
    def test_show(self):
        self.assertNotEqual(instat.show('helloworld'), None, 'show does not create a url')

    def test_search(self):
        self.assertNotEqual(instat.search('helloworld'), None, 'search does not generate media')

    def test_barchart(self):
        instat.barchart([1, 2, 3], [1, 2, 3])

    def test_piechart(self):
        instat.piechart([40, 10, 20, 30], ['Project', 'Homework', 'Midterm', 'Final'], 'PLT Grades')

    def test_linechart(self):
        instat.linechart([1, 2, 3], [1, 2, 3])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBuiltIn)
    unittest.TextTestRunner(verbosity=2).run(suite)