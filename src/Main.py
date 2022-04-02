import cv2

from src.detection.Detection import Detection
import src.tools.Tools as tl


class ControlVisitantes:
    """
    Main class of the project. Inits and executes the application.
    """

    def __init__(self):
        print('TODO')

    def main(self, *args, **kwargs):
        """
        Main class function
        :return: None
        """
        detector = Detection()
        for file, im in tl.load_video('dataset_2/EnterExitCrossingPaths1front.mpg'):
            im, feets = detector.detect(im, paint=True)
            cv2.imshow('frame', im)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    ControlVisitantes().main()
