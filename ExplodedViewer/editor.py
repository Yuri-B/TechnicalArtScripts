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

    slaveControls = cmds.ls("*SLAVE*",transforms=True)
    if len(slaveControls) < 1:
        handleWarning(warningText="please create Slave controls")
        return

    minRandValue = (controlValue * -1) / 10 + 1
    maxRandValue = controlValue

    for item in slaveControls:
        # create a random slider value for each different control
        enterRandomValue = random.uniform(minRandValue,maxRandValue)

        if translateControls == True:
            cmds.setAttr(item +'.positionMultiplier', enterRandomValue)

        if rotateControls == True:
            for axisName in ["X","Y","Z"]:
                cmds.setAttr(item + ".rotate" + axisName, enterRandomValue)

def resetMasterControlPositions():
    masterControls = cmds.ls("*MASTER*",transforms=True)

    # reset positions of X, Y, Z axes controls ( in later releases )
    # reset the attribute "positionMultiplier" on every singe control
    for item in masterControls:
        for axis in ["X","Y","Z"]:
            cmds.setAttr(item +'.translate'+ axis, 0)

def resetSlaveControlPositions():
    slaveControls = cmds.ls("*SLAVE*",shapes=False,transforms=True)

    for item in slaveControls:
        cmds.setAttr(item +'.positionMultiplier', 1)

        #reset rotations
        for axisName in ["X","Y","Z"]:
            cmds.setAttr(item + ".rotate" + axisName, 0)

def proportionalTranslateControls():
    #get world space Translate for each child control
    #rank them from 0 to 10
    #assign a weighted rating to their positionMultiplier attribute
    controlValue = cmds.floatSliderGrp('proportionalTranslate_UIctrl', value=True, query=True)

    slaveControls = cmds.ls("*SLAVE*",shapes=False,transforms=True)
    for item in slaveControls:
        controlCenter = cmds.xform(item, query=True, rotatePivot=True, worldSpace=True)
        #get center of each object

        #get master control position
        masterControl = cmds.ls("*MASTER*",transforms=True)[0]
        masterControlCenter = cmds.xform(masterControl, query=True, rotatePivot=True, worldSpace=True)

        controlDistance = math.sqrt(  math.pow(masterControlCenter[0]-controlCenter[0],2) + math.pow(masterControlCenter[1]-controlCenter[1],2) + math.pow(masterControlCenter[2]-controlCenter[2],2)  )
