import unittest
from src.control import Count, Region


class MyTestCase(unittest.TestCase):
    def test_count(self):
        contador = Count.Count()
        contador.add_region()
        contador.add_ocurrence()
        self.assertEqual(contador.ocurrences(), 1)


