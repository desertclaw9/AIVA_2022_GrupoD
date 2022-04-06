from src.Detection import Detection
import unittest
import src.Tools as tl
import pandas as pd


class DetectionTest(unittest.TestCase):
    def setUp(self):
        self.detector = Detection()
        self.frames = tl.load_video('dataset_2/OneLeaveShop1front.mpg')

    def test_ouput_type(self):
        file, im = next(self.frames)
        im, pd_res = self.detector.predict(im, paint=False)
        self.assertEqual(type(pd_res), pd.DataFrame)

    def test_output(self):
        lenght = 0
        for file, im in self.frames:
            im, pd_res = self.detector.predict(im, paint=False)
            lenght += pd_res.size
        self.assertGreater(lenght, 1)
