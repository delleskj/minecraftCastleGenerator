# https://math.stackexchange.com/questions/4231713/has-anyone-ever-attempted-to-find-all-splits-of-a-rectangle-into-smaller-rectang


from random import randint
from turtle import right
# from pymclevel.box import BoundingBox

def make2dList(nRows, nCols):
	newList = []
	for row in xrange(nRows):
		# give each new row an empty list
		newList.append([])
		for col in xrange(nCols):
			# initialize with 0s
			newList[row].append(0)
			
	return newList


class RectangleSplitter:
	def __init__(self, width, length):
		self._groundMatrix = make2dList(width, length)
		self.newRectMinWidth = 0 #min(width, 3)
		self.newRectMinLength = 0 #min(length, 3)

	# def __init__(self, selectionBox) -> None:
	#     selectionBox = BoundingBox(selectionBox) # DEBUG: to get the class shown correctly in IDE
	#     self._groundMatrix = make2dList(selectionBox.width, selectionBox.length)

	def Partition(self, partitionCount):
		"""
		example groundMatrix:
			y0, y1, y2
		x0  [0 1 2]
		x1  [3 4 5]
		x2  [6 7 8]
		x3  [ 9 10 11]
		Algorithm:
		for n = partitionCount
		- random left or top edge
		- count number of distinct rectangles on that edge + at which index they start
		- random amount of rect to use (full length)
		- push border random % amount in => parameter
		- fill with new index

		"""        
		for n in xrange(1, partitionCount):
			self.CalculatePartition(n)
								
		return self._groundMatrix

	def CalculatePartition(self, n):
		print("partition: " + str(n))
		left = randint(0, 1)
		leftRectStartIndexList = self.GetListOfLeftBorderRectangleStarts()
		leftRectBorderCount = len(leftRectStartIndexList)
		topRectStartIndexList = self.GetListOfTopBorderRectangleStarts()
		topRectBorderCount = len(topRectStartIndexList)
		# add the end of base rectangle as last elements:
		topRectStartIndexList.append(len(self._groundMatrix[0])-1)
		leftRectStartIndexList.append(len(self._groundMatrix)-1)

		print("left List: ")
		print(leftRectStartIndexList)
		print("top List: ")
		print(topRectStartIndexList)
		if(left == 1):
			# push from left
			rectIndex = randint(0, topRectBorderCount)
			newRectMaxX = topRectStartIndexList[rectIndex]-1 # next rect start is the max
			newRectMaxY = randint(self.newRectMinWidth, leftRectStartIndexList[0])          
			print("push from left to x/y: " + str(newRectMaxX) + "/" + str(newRectMaxY))         
		elif(left == 0):
			# push from top
			rectIndex = randint(0, (len(leftRectStartIndexList)-1) )
			newRectMaxX = leftRectStartIndexList[rectIndex]-1 # next rect start is the max
			newRectMaxY = randint(self.newRectMinWidth, topRectStartIndexList[0])
			print("push from top to x/y: " + str(newRectMaxX) + "/" + str(newRectMaxY))         

		self.FillNextPartition(n, newRectMaxX, newRectMaxY)
		# print(self._groundMatrix)

	def FillNextPartition(self, partitionId, maxX, maxY):
		for x in xrange(0, maxX):
			for z in xrange(0, maxY):
				self._groundMatrix[x][z] = partitionId

	def GetListOfTopBorderRectangleStarts(self):
		count = []
		lastRectangleId = -1
		for yi, y in enumerate(self._groundMatrix[0]):
			if(y != lastRectangleId):
				count.append(yi)
				lastRectangleId = y
		count.pop(0) # remove first change
		return count

	def GetListOfLeftBorderRectangleStarts(self):
		count = []
		lastRectangleId = -1
		for yi, y in enumerate(self._groundMatrix):
			if(y[0] != lastRectangleId):
				count.append(yi)
				lastRectangleId = y[0]
		count.pop(0) # remove first change
		return count
