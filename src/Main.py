from src.Detection import Detection
import src.Tools as tl
from src.Control import Control
import cv2
import os


def main():
    """
    Main class function
    :return: None
    """
    detector = Detection()
    controller = Control(maxDisappeared=40, maxDistance=50)
    root = 'dataset_2'
    for path in tl.load_folder(root):
        print('[' + path + ']')
        finish = False
        for file, im in tl.load_video(os.path.join(root, path)):
            im, feets = detector.detect(im, paint=True)
            controller.update(feets)
            controller.counting(im, display=True)
            cv2.imshow('frame', im)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('n'):
                break
            elif key == ord('q'):
                finish = True
                break
        controller.results(path)
        if finish:
            exit(0)


if __name__ == '__main__':
    main()
