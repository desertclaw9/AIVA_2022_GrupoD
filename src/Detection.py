import torch
import src.Tools as tl
import cv2 as cv2


class Detection:
    """
    Defines pytorch model to detect people. Consist on a YOLOv5 pretrained.
    """

    def __init__(self, model='yolov5s'):
        self.model = torch.hub.load('ultralytics/yolov5', model)

    def loadModel(self, model):
        """
        Changes model type of YOLOv5
        :param model: String with name of Model
        :return: None
        """
        self.model = torch.hub.load('ultralytics/yolov5', model)

    def predict(self, im, paint, print=False):
        """
        Predicts input data
        :param print: print info from model or not
        :param im: input image
        :param paint: boolean if result is painted on im or not
        :return: resulting image and pandas dataframe with output info of Persons bounding box
        """
        results = self.model(im)
        if print:
            results.print()
        results_pd = results.pandas().xyxy[0]
        results_pd = results_pd[results_pd['class'] == 0]
        if paint:
            tl.paint_rectangle(im, results_pd)
        return im, results_pd

    def get_feets(self, im, results_pd, paint):
        """
        Given a pandas dataframe with output info of Persons bounding box return its feets
        :param im: input image
        :param results_pd: pandas dataframe with output info of Persons bounding box
        :param paint: boolean if result is painted on im or not
        :return: resulting image and list with position of feets
        """
        feets = []
        for index, row in results_pd.iterrows():
            pt_left = (row['xmin'], row['ymax'])
            pt_right = (row['xmax'], row['ymax'])
            pt_medio = ((pt_left[0] + pt_right[0]) / 2, (pt_left[1] + pt_right[1]) / 2)
            if paint:
                im = cv2.circle(im, (int(pt_medio[0]), int(pt_medio[1])), radius=2, color=(0, 0, 255), thickness=-1)
            feets.append(pt_medio)
        return im, feets

    def detect(self, im, paint=False):
        """
        Given an imagen predicts person's bounding box and calculates its feets position
        :param im: input image
        :param paint: boolean if result is painted on im or not
        :return:
        """
        im, results_pd = self.predict(im, paint)
        im, feets = self.get_feets(im, results_pd, paint)
        return im, feets