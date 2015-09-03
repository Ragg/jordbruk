# coding: utf-8
import unittest
import jordbruk


class TestSplit(unittest.TestCase):
    def test_split(self):
        self.assertEqual(list(jordbruk.split("ku2")), [["ku", "2"]])
        self.assertEqual(list(jordbruk.split("få1 sv1")), [["få", "1"], ["sv", "1"], ])
        self.assertEqual(list(jordbruk.split("hv1/4 ru1/2 ha2 po3")),
                         [["hv", "1/4"], ["ru", "1/2"], ["ha", "2"], ["po", "3"], ])
        self.assertEqual(list(jordbruk.split("hv3/8 ru1/2 by1/2 ha3 er1/8 po3")),
                         [["hv", "3/8"], ["ru", "1/2"], ["by", "1/2"], ["ha", "3"], ["er", "1/8"], ["po", "3"], ])
        self.assertEqual(list(jordbruk.split("hv%1/4% ru%1/4% by%3/4% ha%1 1/2% po%5%")),
                         [["hv", "1/4"], ["ru", "1/4"], ["by", "3/4"], ["ha", "1 1/2"], ["po", "5"], ])
        self.assertEqual(list(jordbruk.split("kuKoe")), [])
        self.assertEqual(list(jordbruk.split("ha22!!")), [])

if __name__ == '__main__':
    unittest.main()
