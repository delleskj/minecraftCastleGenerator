# this filter: creates a castle

from operator import le
import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from turtle import width
from unittest import case
from click import option
from numpy import *
from sqlalchemy import true
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
from pymclevel.box import Vector

import utilityFunctions as utilityFunctions

#inputs are taken from the user. Here I've just showing labels, as well as letting the user define
# what the main creation material for the structures is
inputs = (
	("Castle creation", "label"),
	("Creator: Jonas Delleske", "label"),
	("WallMaterial", alphaMaterials.Cobblestone), # the material we want to use to build the mass of the structures
	("WallWidth", 2),
	)

class CastleConfig:
	maxWallHeight = 7
	mainGateWidth = 4
	mainGateMinHeight = 3

# MAIN SECTION #
# Every agent must have a "perform" function, which has three parameters
# 1: the level (aka the minecraft world). 2: the selected box from mcedit. 3: User defined inputs from mcedit
def perform(level, selectionBox, options):
	# some config
	config = CastleConfig()
	wallMaterialId = options["WallMaterial"].ID
	outerWallWidth = int(options["WallWidth"])

	selectionBox = BoundingBox(selectionBox) # DEBUG: to get the class shown correctly in IDE
	clearBox(level, selectionBox)

	# outer walls
	outerBox = BoundingBox(selectionBox.origin, (selectionBox.size.x, min(selectionBox.size.y-1, config.maxWallHeight), selectionBox.size.z))
	buildWalls(level, outerBox, wallMaterialId, 1)	
	buildBattlements(level, outerBox, wallMaterialId)
	# outer wall thickness
	innerBox = BoundingBox(outerBox.origin, (outerBox.size.x,outerBox.size.y-1,outerBox.size.z))
	innerBox = innerBox.expand(-1,0,-1)
	buildWalls(level, innerBox, wallMaterialId, outerWallWidth-1)

	# gate
	gateBox = decideGatePosition(selectionBox, outerWallWidth, config.mainGateWidth, randint(config.mainGateMinHeight, outerBox.height-2))
	buildGate(level, gateBox, wallMaterialId)

	# keep
	indentFromSelectionBox = outerWallWidth + 4
	keepBox = outerBox.expand(-indentFromSelectionBox,0,-indentFromSelectionBox)
	keepBox = randomBoxFromSelection(keepBox,10,15,4,selectionBox.height,10,15)
	buildWalls(level, keepBox, wallMaterialId, 1)
	keepGate = decideGatePosition(keepBox, 1, 2, 2)
	buildGate(level, keepGate, wallMaterialId)
	keepRoof = BoundingBox( (keepBox.origin.x, keepBox.maxy-2, keepBox.origin.z), (keepBox.size.x,1,keepBox.size.z))
	fillBox(level, keepRoof, wallMaterialId, True)

	# tower
	for x in range(1, 10):
		towerBox = randomBoxFromSelection(selectionBox,4,4,5,selectionBox.height-1,4,4)
		buildWalls(level, towerBox, wallMaterialId, 1)
		buildBattlements(level, towerBox, wallMaterialId)

def decideGatePosition(box, wallWidth, gateWidth, gateHeight):
	box = BoundingBox(box) # DEBUG: to get the class shown correctly in IDE
	height = gateHeight
	#gateWidth = 4
	x = 0
	z = 0
	xWidth = 0
	zWidth = 0

	side = randint(0,3)
	if(side==0):
		# west
		x = box.minx
		z = randint(box.minz, box.maxz-1-gateWidth)
		xWidth = wallWidth
		zWidth = gateWidth
	if(side==1):
		# east
		x = box.maxx - wallWidth
		z = randint(box.minz, box.maxz-1-gateWidth) - gateWidth
		xWidth = wallWidth
		zWidth = gateWidth
	if(side==2):
		# south
		x = randint(box.minx, box.maxx-1-gateWidth)
		z = box.minz
		xWidth = gateWidth
		zWidth = wallWidth
	if(side==3):
		# north
		x = randint(box.minx, box.maxx-1-gateWidth) - gateWidth
		z = box.maxz - wallWidth
		xWidth = gateWidth
		zWidth = wallWidth
	return BoundingBox((x,box.miny,z), (xWidth,height,zWidth))



def buildGate(level, box, materialId):
	clearBox(level, box)

def buildBattlements(level, box, materialId):
	"""
	places battlements along the box border on top of the box (at maxy level)
	"""
	newValue = 0	
	yLevel = box.maxy
	for x in range(box.minx, box.maxx):			
		for z in range(box.minz, box.maxz):			
			if(x==box.minx or x==box.maxx-1 or z==box.minz or z==box.maxz-1):
				if(x==box.minx or x==box.maxx-1):
					if((z % 2) == 0):
						utilityFunctions.setBlock(level, (materialId, newValue), x, yLevel, z)				
				if(z==box.minz or z==box.maxz-1):
					if((x % 2) == 0):
						utilityFunctions.setBlock(level, (materialId, newValue), x, yLevel, z)
								

def buildWalls(level, box, materialId, width):
	box = BoundingBox(box) # DEBUG: to get the class shown correctly in IDE

	# build a wall along the borders of the box
	height = box.height
	topWall = BoundingBox((box.minx, box.miny, box.minz), (box.size.x, height, width))
	botWall = BoundingBox((box.minx, box.miny, box.maxz-width), (box.size.x, height, width))
	fillBox(level, topWall, materialId, True)
	fillBox(level, botWall, materialId, True)

	leftWall = BoundingBox((box.minx, box.miny, box.minz), (width, height, box.size.z))
	rightWall = BoundingBox((box.maxx-width, box.miny, box.minz), (width, height, box.size.z))
	fillBox(level, leftWall, materialId, True)
	fillBox(level, rightWall, materialId, True)

	
# fills the given box with wall
def generateWall(level, box, materialId):	
	fillBox(level, box, materialId, True)

# fills given box with air
def clearBox(level, box):
	fillBox(level, box, 0, True)

# fills given box with given material, overwrites existing blocks if overwriteExisting = True
def fillBox(level, box, materialId, overwriteExisting):
	newValue = 0	
	for y in range(box.miny, box.maxy):
		for x in range(box.minx, box.maxx):			
			for z in range(box.minz, box.maxz):
				if(overwriteExisting):
					utilityFunctions.setBlock(level, (materialId, newValue), x, y, z)
				else:
					utilityFunctions.setBlockIfEmpty(level, (materialId, newValue), x, y, z)


def randomBoxFromSelection(selectionBox, minX, maxX, minY, maxY, minZ, maxZ):
	"""
	get a random positioned box within the selectionBox
	based on ground plane of given box
	"""
	maxX = min(selectionBox.size.x, maxX)
	maxY = min(selectionBox.size.y, maxY)
	maxZ = min(selectionBox.size.z, maxZ)
	selectionBox = BoundingBox(selectionBox) # DEBUG: to get the class shown correctly in IDE
	newBoxWidth = randint(minX, maxX)
	newBoxHeight = randint(minY, maxY)
	newBoxLength = randint(minZ, maxZ)
	newx = randint(selectionBox.origin.x, selectionBox.maxx-newBoxWidth)
	newy = selectionBox.origin.y
	newz = randint(selectionBox.origin.z, selectionBox.maxz-newBoxLength)
	newOrigin = Vector(newx,newy,newz)
	return BoundingBox( newOrigin, (newBoxWidth, newBoxHeight,  newBoxLength))