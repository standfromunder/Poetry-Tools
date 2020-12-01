import os
import unittest
from poetrytools.PoetryRU import PoetryRU


class TestENPoems(unittest.TestCase):
    def setUp(self):
        self.poetryRUS = PoetryRU('cmudict/ru_cmudict.json')

    def open_poem(self, poem):
        with open(os.path.join('..','poems', 'ru', poem)) as f:
            return self.poetryRUS.tokenize(f.read())

    def test_rhyme_1(self):
        self.assertTrue(self.poetryRUS.rhymes('логопед', 'мопед'))

    def test_poem_1(self):
        rhyme_scheme_string, rhyme = self.poetryRUS.guess_rhyme_type(self.open_poem('test1.txt'))
        self.assertTrue(rhyme_scheme_string == 'aabb')



if __name__ == '__main__':
    unittest.main()
