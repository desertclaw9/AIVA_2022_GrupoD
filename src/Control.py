from src.Centroidtracking import CentroidTracking
import numpy as np
import cv2


class Control:
    def __init__(self, maxDisappeared=40, maxDistance=50):
        self.totalDown = 0
        self.totalUp = 0
        self.totalRight = 0
        self.totalLeft = 0
        self.totalLeft2 = 0
        self.totalRight2 = 0
        self.stop = 0
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
                # if not trck_obj.counted or trck_obj.counted:
                # If the direction is negative (indicating the object is moving up) AND the centroid is above the center
                # line, count the object
                if not trck_obj.upCounted and y_direction < 0 and (round(height / 2) - 5) - 5 < centroid[1] < (
                        round(height / 2) - 5) + 5:
                    self.totalUp += 1
                    trck_obj.upCounted = True
                elif not trck_obj.downCounted and y_direction > 0 and (round(height / 2) - 5) - 5 < centroid[1] < (
                        round(height / 2) - 5) + 5:
                    self.totalDown += 1
                    trck_obj.downCounted = True
                elif not trck_obj.rightCounted and x_direction > 0 and round(width / 2) < centroid[0] < round(
                        width / 2) + 20:
                    self.totalRight += 1
                    trck_obj.rightCounted = True
                elif not trck_obj.leftCounted and x_direction < 0 and round(width / 2) < centroid[0] < round(
                        width / 2) + 35:
                    self.totalLeft += 1
                    trck_obj.leftCounted = True
                    trck_obj.frameCount = 0
                elif not trck_obj.secondLeftCounted and x_direction < 0 and 40 < centroid[0] < 80:
                    trck_obj.secondLeftCounted = True
                    self.totalLeft2 += 1
                elif not trck_obj.secondLeftCounted and x_direction > 0 and 40 < centroid[0] < 80:
                    trck_obj.secondRightCounted = True
                    self.totalRight2 += 1

                trck_obj.frameCount += 1

                if not trck_obj.stopped and trck_obj.leftCounted and not trck_obj.secondLeftCounted and trck_obj.frameCount > 140:
                    self.stop += 1
                    trck_obj.stopped = True
                    trck_obj.frameCount = 0

                if not trck_obj.stopped and not trck_obj.rightCounted and trck_obj.secondRightCounted and trck_obj.frameCount > 140:
                    self.stop += 1
                    trck_obj.stopped = True
                    trck_obj.frameCount = 0

                # if trck_obj.leftCounted and not trck_obj.secondleftCounted:
                # trck_obj.frameCount = 0

            # Store the trackable object in the dictionary
            self.trackableObjects[objectID] = trck_obj

        if display:
            # Information that will be displayed on the frame
            info = [
                ("Stop", self.stop),
                ("Up", self.totalUp),
                ("Down", self.totalDown),
                ("Right", self.totalRight),
                ("Left", self.totalLeft)
                #("2LinetoLeft", self.totalLeft2),
                #("1LinetoRight", self.totalRight2)
            ]
            # Draw the info in our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, height - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    def update(self, inputCentroids):
        self.objects = self.centroid_tracker.update(inputCentroids)

    def results(self):
        entran = self.totalUp
        salen = self.totalDown
        pasan = (self.totalLeft + self.totalRight) - (entran) - salen - (self.stop) if (self.totalLeft + self.totalRight) - (entran) - salen - (self.stop)  > 0 else 0
        tienda = self.stop

        self.totalLeft = 0
        self.totalUp = 0
        self.totalRight = 0
        self.totalDown = 0
        self.totalLeft2 = 0
        self.totalRight2 = 0
        self.stop = 0

        return entran, salen, pasan, tienda


class TrackableObject:
    """
    Defines the attributes of an object, objectID, centroid and if it has been counted or not
    """

    def __init__(self, objectID, centroid):
        self.objectID = objectID
        self.centroids = [centroid]
        self.counted = False
        self.rightCounted = False
        self.leftCounted = False
        self.secondLeftCounted = False
        self.secondRightCounted = False
        self.stopped = False
        self.upCounted = False
        self.downCounted = False
        self.frameCount = 0
