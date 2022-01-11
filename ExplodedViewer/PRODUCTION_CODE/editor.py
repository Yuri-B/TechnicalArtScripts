import maya.cmds as cmds
import random
import math

# CONTROLLERS

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
            hasPositionMultiplier = cmds.listAttr(item,string="positionMultiplier")
            if hasPositionMultiplier:
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
            try:
                cmds.setAttr(item +'.translate'+ axis, 0)
            except:
                #if object has locked attributes, do not reset controls
                print("this object has locked attributes")

        hasPositionMultiplier = cmds.listAttr(item,string="positionMultiplier")
        if hasPositionMultiplier:
            cmds.setAttr(item +'.positionMultiplier', 1)

def resetControlRotations():
    controls = cmds.ls(shapes=False,transforms=True,selection=True)

    for item in controls:
        #reset rotations
        for axisName in ["X","Y","Z"]:
            cmds.setAttr(item + ".rotate" + axisName, 0)

def proportionalControls():
    #get world space Translate for each child control
    #save distance between center of master control and world space Translate for each child control into an array
    #assign a weighted rating to their positionMultiplier attribute. Weighted rating is relative to the child control which has the highest distance between itself and master control
    controlValue = cmds.floatSliderGrp('proportionalTranslate_UIctrl', value=True, query=True)
    #test controlValue = 3

    distanceRankingArray = []
    selectedControls = cmds.ls(shapes=False,transforms=True,selection=True)
    for item in selectedControls:
        #get center of each child control
        controlCenter = cmds.xform(item, query=True, rotatePivot=True, worldSpace=True)

        #get center of master control that is a parent of child control
        masterControlObject = cmds.listRelatives(item, parent=True)
        masterControl = cmds.ls(masterControlObject,transforms=True)
        masterControlCenter = cmds.xform(masterControl, query=True, rotatePivot=True, worldSpace=True)

        #find distance between center of master control and child control
        controlDistance = math.sqrt(  math.pow(masterControlCenter[0]-controlCenter[0],2) + math.pow(masterControlCenter[1]-controlCenter[1],2) + math.pow(masterControlCenter[2]-controlCenter[2],2)  )
        #save all the distances to the distanceRankingArray to determine the maximum distance and minimum distance.
        distanceRankingArray.append(controlDistance)

    highestDistance = max(distanceRankingArray)

    # first item in selection has been assigned to DistanceRankingArray as first item, so the object index in DistanceRankingArray and selection match perfectly
    for item in selectedControls:
        hasPositionMultiplier = cmds.listAttr(item,string="positionMultiplier")
        if hasPositionMultiplier:
            itemIndex = selectedControls.index(item)

            #weighted rating = distance between specific child control and master control : highest distance from arrat
            multiplierValue = controlValue * ( distanceRankingArray[itemIndex] / highestDistance )
            cmds.setAttr(item +'.positionMultiplier', multiplierValue)
