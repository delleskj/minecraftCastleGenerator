# https://math.stackexchange.com/questions/4231713/has-anyone-ever-attempted-to-find-all-splits-of-a-rectangle-into-smaller-rectang


# from random import randint
from numpy import random
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
        self.newRectMinWidth = 0  # min(width, 3)
        self.newRectMinLength = 0  # min(length, 3)
        # docs: https://numpy.org/doc/stable/reference/random/legacy.html#numpy.random.RandomState
        # distribution graphs: https://statdist.com/
        self.randomState = random.RandomState()

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
        # left = self.randomState.randint(0, 2)
        left = n % 2
        leftRectStartList = self.GetListOfLeftBorderRectangleStarts()
        leftRectBorderCount = len(leftRectStartList)
        topRectStartList = self.GetListOfTopBorderRectangleStarts()
        topRectBorderCount = len(topRectStartList)
        # add the end of base rectangle as last elements:
        topRectStartList.append(len(self._groundMatrix[0]))
        leftRectStartList.append(len(self._groundMatrix))

        print("left List: " + str(leftRectBorderCount))
        print(leftRectStartList)
        print("top List: " + str(topRectBorderCount))
        print(topRectStartList)
        if left == 1:
            # push from left
            rectIndex = self.GetRandomPushy(0, topRectBorderCount)
            min_width = 0  # max(self.newRectMinWidth, leftRectStartList[0]-1)
            newRectMaxX = self.GetRandomNormal(min_width, leftRectStartList[0] - 1)
            newRectMaxY = topRectStartList[rectIndex]-1  # next rect start is the max
            print("push from left to x/y: " + str(newRectMaxX) + "/" + str(newRectMaxY))
        elif left == 0:
            # push from top
            rectIndex = self.GetRandomPushy(0, leftRectBorderCount)
            newRectMaxX = leftRectStartList[rectIndex]-1  # next rect start is the max
            min_width = 0  # max(self.newRectMinWidth, leftRectStartList[0] - 1)
            newRectMaxY = self.GetRandomNormal(min_width, topRectStartList[0] - 1)
            print("push from top to x/y: " + str(newRectMaxX) + "/" + str(newRectMaxY))

        self.FillNextPartition(n, newRectMaxX, newRectMaxY)

    # print(self._groundMatrix)

    def FillNextPartition(self, partitionId, maxX, maxY):
        for x in xrange(0, maxX + 1):
            for z in xrange(0, maxY + 1):
                self._groundMatrix[x][z] = partitionId

    def GetListOfTopBorderRectangleStarts(self):
        count = []
        lastRectangleId = -1
        for yi, y in enumerate(self._groundMatrix[0]):
            if y != lastRectangleId:
                count.append(yi)
                lastRectangleId = y
        count.pop(0)  # remove first change
        return count

    def GetListOfLeftBorderRectangleStarts(self):
        count = []
        lastRectangleId = -1
        for yi, y in enumerate(self._groundMatrix):
            if y[0] != lastRectangleId:
                count.append(yi)
                lastRectangleId = y[0]
        count.pop(0)  # remove first change
        return count

    def GetRandomPushy(self, start, end):
        if end <= start:
            return start
        value = self.randomState.beta(4, 2)
        # value = self.randomState.normal(0.5, 0.1)
        # value = self.randomState.beta(1, 1)  # uniform
        print ("rand value between " + str(start) + " end " + str(end) + " is: " + str(value))
        value = int(round(start + (value / float(1 / float(end - start)))))
        print ("rand value between " + str(start) + " end " + str(end) + " is: " + str(value))
        return value

    def GetRandomNormal(self, start, end):
        if end <= start:
            return start
        # value = self.randomState.beta(2, 4)
        value = self.randomState.normal(0.5, 0.1)
        # value = self.randomState.beta(1, 1)  # uniform
        print ("rand value between " + str(start) + " end " + str(end) + " is: " + str(value))
        value = int(round(start + (value / float(1 / float(end - start)))))
        print ("rand value between " + str(start) + " end " + str(end) + " is: " + str(value))
        return value
