import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest

from rhymes import approx_nsyl
from rhymes import nsyl
from rhymes import rhymesyls


class test_nsyl(unittest.TestCase):

    def test_nsyl_counter(self):
        self.assertEqual(nsyl("testing"),2)
        self.assertEqual(nsyl("fred"),1)
        self.assertEqual(nsyl("pigsty"),2)
        self.assertEqual(nsyl("difficult"),3)

    def test_rhymesyls(self):
        self.assertEqual(rhymesyls("pie"),rhymesyls("sty"))
        self.assertNotEqual(rhymesyls("pie"),rhymesyls("bed"))
        self.assertEqual(rhymesyls("fated"),rhymesyls("mated"))
        # TODO: get this test to pass:
        # self.assertEqual(rhymesyls("hated"),rhymesyls("mated"))

if __name__ == '__main__':
    unittest.main()
