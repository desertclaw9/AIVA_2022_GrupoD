from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class CentroidTracking:
	"""
	Defines the register, deregister and update of an object and its centroid.
	"""
	def __init__(self, maxDisappeared=50, maxDistance=50):
		self.nextObjectID = 0
		self.objects = OrderedDict()
		self.disappeared = OrderedDict()

		# Store the number of maximum consecutive frames a given bject is allowed to be marked as "disappeared" until we
		# need to deregister the object from tracking
		self.maxDisappeared = maxDisappeared

		# Store the maximum distance between centroids to associate an object
		self.maxDistance = maxDistance

	def register(self, centroid):
		"""
		Register a new object with the next available object ID to store the centroid
		:param centroid:
		:return: -
		"""
		self.objects[self.nextObjectID] = centroid
		self.disappeared[self.nextObjectID] = 0
		self.nextObjectID += 1

	def deregister(self, objectID):
		"""
		Deregister an object ID by deleting it from both dictionaries
		:param objectID: object ID to delete
		:return: -
		"""
		del self.objects[objectID]
		del self.disappeared[objectID]

	def update(self, inputCentroids):
		"""

		:param inputCentroids:
		:return:
		"""
		# Check to see if the list of input centroids is empty
		if len(inputCentroids) == 0:
			# Loop over any existing tracked objects and mark them as disappeared
			for objectID in list(self.disappeared.keys()):
				self.disappeared[objectID] += 1

				# Deregister an object if it has reached a maximum number of consecutive frames marked as missing
				if self.disappeared[objectID] > self.maxDisappeared:
					self.deregister(objectID)

			# Return objects if there are no centroids or tracking info to update
			return self.objects

		# If we are not tracking any object take the input centroids and register each of them
		if len(self.objects) == 0:
			for i in range(0, len(inputCentroids)):
				self.register(inputCentroids[i])

		# Otherwise there are currently tracking objects --> try to match the input centroids to existing object centroids
		else:
			# Grab the set of object IDs and corresponding centroids
			objectIDs = list(self.objects.keys())
			objectCentroids = list(self.objects.values())

			# Compute the distance between each pair of object centroids and input centroids
			# The goal is to match an input centroid to an existing object centroid
			D = dist.cdist(np.array(objectCentroids), inputCentroids)

			# Matching -> 1) Find the smallest value in each row, 2) sort the row indexes based on
			# their minimum values so that the row with the smallest value is at the *front* of the index list
			rows = D.min(axis=1).argsort()

			# Same with the columns and then sorting using the previously computed row index list
			cols = D.argmin(axis=1)[rows]

			# Keep track of which of the rows and column indexes we have already examined
			usedRows = set()
			usedCols = set()

			# Loop over the combination of the (row, column) index tuples
			for (row, col) in zip(rows, cols):
				# If we have already examined either the row or column value before --> ignore it
				if row in usedRows or col in usedCols:
					continue
				# If the distance between centroids is greater than the maximum distance --> Do not associate the two centroids to the same object
				if D[row, col] > self.maxDistance:
					continue

				# Otherwise, grab the object ID for the current row, set its new centroid, and reset the disappeared counter
				objectID = objectIDs[row]
				self.objects[objectID] = inputCentroids[col]
				self.disappeared[objectID] = 0

				# Indicate that we have examined each of the row and column indexes
				usedRows.add(row)
				usedCols.add(col)

			# Compute both the row and column index we have NOT yet examined
			unusedRows = set(range(0, D.shape[0])).difference(usedRows)
			unusedCols = set(range(0, D.shape[1])).difference(usedCols)

			# If the number of object centroids is equal or greater than the number of input centroids
			# Check and see if some of these objects have potentially disappeared
			if D.shape[0] >= D.shape[1]:
				# Loop over the unused row indexes
				for row in unusedRows:
					# Grab the object ID for the corresponding row index and increment the disappeared counter
					objectID = objectIDs[row]
					self.disappeared[objectID] += 1
					# Check to see if the number of consecutive frames the object has been marked "disappeared"
					# for warrants deregistering the object
					if self.disappeared[objectID] > self.maxDisappeared:
						self.deregister(objectID)

			# If the number of input centroids is greater than the number of existing object centroids -->
			# Register each new input centroid as a trackable object
			else:
				for col in unusedCols:
					self.register(inputCentroids[col])

		# Return the set of trackable objects
		return self.objects