import unittest
import src.Tools as tl


class ToolsTest(unittest.TestCase):
    def test_load_data(self):
        for file, im in tl.load_video('dataset_2/OneLeaveShop1front.mpg'):
            self.assertIsNotNone(im)
