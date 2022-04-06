import cv2
from src.Detection import Detection
import src.Tools as tl
from src.Centroidtracking import CentroidTracking
from src.Trackableobject import TrackableObject
import numpy as np

totalDown = 0
totalUp = 0
totalRight = 0
totalLeft = 0
trackers = []
trackableObjects = {}


def counting(objects, frame):
    """
    Function to count the people based on the direction and position of the feet
    :param objects: objects
    :param frame: frame to process
    :return:
    """

    height = frame.shape[0]
    width = frame.shape[1]

    global totalDown
    global totalUp
    global totalRight
    global totalLeft

    # Loop over the tracked objects
    for (objectID, centroid) in objects.items():
        # Check to see if a trackable object exists for the current object ID
        trck_obj = trackableObjects.get(objectID, None)
        # If there is no existing trackable object --> Create one
        if trck_obj is None:
            trck_obj = TrackableObject(objectID, centroid)
        # Otherwise, there is a trackable object so we can determine the direction
        else:
            # Calculate the difference between the y-coordinate of the *current* centroid and the mean of previous
            # centroids --> tell us in which direction the object is moving
            # Negative --> 'up' and positive --> 'down')
            y = [c[1] for c in trck_obj.centroids]
            x = [c[0] for c in trck_obj.centroids]
            y_direction = centroid[1] - np.mean(y)
            x_direction = centroid[0] - np.mean(x)
            trck_obj.centroids.append(centroid)
            # Check to see if the object has been counted or not
            if not trck_obj.counted:
                # If the direction is negative (indicating the object is moving up) AND the centroid is above the center
                # line, count the object
                if y_direction < 0 and round(height / 2) - 5 < centroid[1] < round(height / 2) + 5:
                    totalUp += 1
                    trck_obj.counted = True
                elif y_direction > 0 and round(height / 2) - 5 < centroid[1] < round(height / 2) + 5:
                    totalDown += 1
                    trck_obj.counted = True
                elif x_direction > 0 and round(width / 2) < centroid[0] < round(width / 2) + 40:
                    totalRight += 1
                    trck_obj.counted = True
                elif x_direction < 0 and round(width / 2) < centroid[0] < round(width / 2) + 40:
                    totalLeft += 1
                    trck_obj.counted = True

        # Store the trackable object in the dictionary
        trackableObjects[objectID] = trck_obj

    # Information that will be displayed on the frame
    info = [
        ("Up", totalUp),
        ("Down", totalDown),
        ("Right", totalRight),
        ("Left", totalLeft)
    ]
    # Draw the info in our frame
    for (i, (k, v)) in enumerate(info):
        text = "{}: {}".format(k, v)
        cv2.putText(frame, text, (10, height - ((i * 20) + 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)


def main():
    """
    Main class function
    :return: None
    """
    detector = Detection()
    centroid_tracker = CentroidTracking(maxDisappeared=40, maxDistance=50)
    for file, im in tl.load_video('dataset_2/OneLeaveShop1front.mpg'):
        im, feets = detector.detect(im, paint=True)
        objects = centroid_tracker.update(feets)
        counting(objects, im)
        cv2.imshow('frame', im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()
