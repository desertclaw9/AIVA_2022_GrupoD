import unittest
from src.Control import Control
from src.Detection import Detection
import src.Tools as tl
import os
import json


class ControlTest(unittest.TestCase):
    def setUp(self):
        self.detector = Detection()
        self.controller = Control(maxDisappeared=40, maxDistance=50)

    def test_easy(self):
        for file, im in tl.load_video('dataset_2/OneLeaveShop1front.mpg'):
            im, feets = self.detector.detect(im, paint=False)
            self.controller.update(feets)
            self.controller.counting(im, display=False)
        result = self.controller.results()
        self.assertEqual((0, 1, 0, 0), result)

    def test_complete(self):
        root = 'dataset_2'
        with open('test/groundtruth.json', 'r') as j:
            gt = json.loads(j.read())
        for path in tl.load_folder(root):
            for file, im in tl.load_video(os.path.join(root, path)):
                im, feets = self.detector.detect(im, paint=True)
                self.controller.update(feets)
                self.controller.counting(im, display=True)
            self.assertEqual(list(self.controller.results()), gt[path], msg=path)
