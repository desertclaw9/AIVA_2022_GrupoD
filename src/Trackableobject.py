
class TrackableObject:
    """
    Defines the attributes of an object, objectID, centroid and if it has been counted or not
    """
    def __init__(self, objectID, centroid):
        self.objectID = objectID
        self.centroids = [centroid]
        self.counted = False
