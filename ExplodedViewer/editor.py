import maya.cmds as cmds
import random
import math

def handleWarning(warningText):
    #cmds.popupMenu(label="foo")
    print warningText

def randomizeChildControls():
    controlValue = cmds.floatSliderGrp('positionRandomizer_UIctrl', value=True, query=True)

    translateControls = True
    rotateControls = False
    handleRandomizer(translateControls, rotateControls, controlValue)

def randomizeRotationChildControls():
    controlValue = cmds.floatSliderGrp('rotationRandomizer_UIctrl', value=True, query=True)

    translateControls = False
    rotateControls = True
    handleRandomizer(translateControls, rotateControls, controlValue)

def handleRandomizer(translateControls, rotateControls, controlValue):

    controls = cmds.ls(transforms=True, selection=True)
    if len(controls) < 1:
        handleWarning(warningText="please select controls")
        return

    minRandValue = (controlValue * -1) / 10 + 1
    maxRandValue = controlValue

    for item in controls:
        # create a random slider value for each different control
        enterRandomValue = random.uniform(minRandValue,maxRandValue)

        if translateControls == True:
            cmds.setAttr(item +'.positionMultiplier', enterRandomValue)

        if rotateControls == True:
            for axisName in ["X","Y","Z"]:
                cmds.setAttr(item + ".rotate" + axisName, enterRandomValue)

def resetControlPositions():
    controls = cmds.ls(transforms=True,selection=True)

    # reset positions of X, Y, Z axes controls ( in later releases )
    # reset the attribute "positionMultiplier" on every singe control
    for item in controls:
        for axis in ["X","Y","Z"]:
            cmds.setAttr(item +'.translate'+ axis, 0)

            #FIX BUG HERE - EXCLUDE OBJECTS THAT DON't HAVE THIS ATTRIBUTE --- EXCLUDE
            cmds.setAttr(item +'.positionMultiplier', 1)

def resetControlRotations():
    controls = cmds.ls(shapes=False,transforms=True,selection=True)

    for item in controls:
        #reset rotations
        for axisName in ["X","Y","Z"]:
            cmds.setAttr(item + ".rotate" + axisName, 0)

def proportionalControls():
    #get world space Translate for each child control
    #rank them from 0 to 10
    #assign a weighted rating to their positionMultiplier attribute
    controlValue = cmds.floatSliderGrp('proportionalTranslate_UIctrl', value=True, query=True)
    #test controlValue = 3

    # FIX BUGS HERE :::::: 
    distanceRankingArray = []
    selectedControls = cmds.ls(shapes=False,transforms=True,selection=True)
    for item in selectedControls:
        controlCenter = cmds.xform(item, query=True, rotatePivot=True, worldSpace=True)
        #get center of each object

        #get master control position - get parent
        masterControlObject = cmds.listRelatives(item, parent=True)
        masterControl = cmds.ls(masterControlObject,transforms=True)[0]
        masterControlCenter = cmds.xform(masterControl, query=True, rotatePivot=True, worldSpace=True)

        controlDistance = math.sqrt(  math.pow(masterControlCenter[0]-controlCenter[0],2) + math.pow(masterControlCenter[1]-controlCenter[1],2) + math.pow(masterControlCenter[2]-controlCenter[2],2)  )
        #add all the distances to the distanceRankingArray to determine the maximum distance and minimum distance.
        distanceRankingArray.append(controlDistance)

    highestDistance = max(distanceRankingArray)

    # set attribute to their multipliers
    for item in slaveControls:
        itemIndex = slaveControls.index(item)

        multiplierValue = controlValue * ( distanceRankingArray[itemIndex] / highestDistance )
        cmds.setAttr(item +'.positionMultiplier', multiplierValue)
