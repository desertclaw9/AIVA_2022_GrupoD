import unittest
import numpy as np


class ToolsTest(unittest.TestCase):
    def test_load_data(self):
        loader = LoadData.LoadData()
        frame = loader.get_frame()
        self.assertEqual(frame, np.array([1, 1, 1, 1]))
