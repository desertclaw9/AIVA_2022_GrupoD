from src.Centroidtracking import CentroidTracking
from src.Trackableobject import TrackableObject
import numpy as np
import cv2


class Control:
    def __init__(self, maxDisappeared=40, maxDistance=50):
        self.totalDown = 0
        self.totalUp = 0
        self.totalRight = 0
        self.totalLeft = 0
        self.trackers = []
        self.trackableObjects = {}
        self.centroid_tracker = CentroidTracking(maxDisappeared=maxDisappeared, maxDistance=maxDistance)
        self.objects = None

    def counting(self, frame, display=False):
        """
        Function to count the people based on the direction and position of the feet
        :param display: Bool if info is displayed on screen or not
        :param objects: objects
        :param frame: frame to process
        :return:
        """

        height = frame.shape[0]
        width = frame.shape[1]
        if self.objects is None:
            print('Call update first!')
            exit(1)
        # Loop over the tracked objects
        for (objectID, centroid) in self.objects.items():
            # Check to see if a trackable object exists for the current object ID
            trck_obj = self.trackableObjects.get(objectID, None)
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
                        self.totalUp += 1
                        trck_obj.counted = True
                    elif y_direction > 0 and round(height / 2) - 5 < centroid[1] < round(height / 2) + 5:
                        self.totalDown += 1
                        trck_obj.counted = True
                    elif x_direction > 0 and round(width / 2) < centroid[0] < round(width / 2) + 40:
                        self.totalRight += 1
                        trck_obj.counted = True
                    elif x_direction < 0 and round(width / 2) < centroid[0] < round(width / 2) + 40:
                        self.totalLeft += 1
                        trck_obj.counted = True

            # Store the trackable object in the dictionary
            self.trackableObjects[objectID] = trck_obj

        if display:
            # Information that will be displayed on the frame
            info = [
                ("Up", self.totalUp),
                ("Down", self.totalDown),
                ("Right", self.totalRight),
                ("Left", self.totalLeft)
            ]
            # Draw the info in our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, height - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    def update(self, inputCentroids):
        self.objects = self.centroid_tracker.update(inputCentroids)

    def results(self, path):
        entran = self.totalUp
        salen = self.totalDown
        pasan = self.totalLeft - (entran + salen) if self.totalLeft - (entran + salen) > 0 else 0
        tienda = 0  # TODO
        print('[' + path + ']')
        print('Entran %d\nSalen %d\nPasan %d\nEscaparate %d' % (entran, salen, pasan, tienda))
        self.totalLeft = 0
        self.totalUp = 0
        self.totalRight = 0
        self.totalDown = 0
