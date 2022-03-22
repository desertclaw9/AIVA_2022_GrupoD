import unittest
from src.detection import Model, Dataset
import numpy as np
import tensorflow as tf


class DetectionTest(tf.test.TestCase):
    def test_ouput_size(self):
        shape = (1, 17)
        model = Model.Model()
        image = model.predict()
        self.assertEqual(image.shape, shape)

    def test_dataset(self):
        dataset = Dataset.Dataset()
        train = dataset.get_train().cardinality().numpy()
        test = dataset.get_test().cardinality().numpy()
        val = dataset.get_val().cardinality().numpy()
        total = train + test + val
        self.assertEqual(train, total * 0.70)
        self.assertEqual(test, total * 0.2)
        self.assertEqual(val, total * 0.1)
