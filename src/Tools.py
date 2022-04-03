import os
import cv2


def load_video(file):
    """
    Splits video into frames
    :return: a list of frames
    """
    cap = cv2.VideoCapture(file)
    while True:
        ret, im = cap.read()
        if not ret:
            print('End of video')
            break
        yield file, im


def load_folder(path):
    """
    Load all videos in a folder
    :return: a list of video paths
    """
    for file in os.listdir(path):
        yield load_video(os.path.join(path, file))


def paint_rectangle(im, pd_results):
    """
    Function that paints bounding boxes predicted from model
    :param im: input image
    :param pd_results: pandas dataframe with output info of Persons bounding box
    :return: resulting image
    """
    for index, row in pd_results.iterrows():
        pt_min = (int(row['xmin']), int(row['ymin']))
        pt_max = (int(row['xmax']), int(row['ymax']))
        im = cv2.rectangle(im, pt_min, pt_max, (0, 255, 0), 2)
    return im