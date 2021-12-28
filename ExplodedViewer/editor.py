import maya.cmds as cmds
import random

def test(*args)
    print "TESTING"

def handleWarning(warningText):
    #cmds.popupMenu(label="foo")
    print warningText

def randomizeChildControls(*args):
    controlValue = cmds.floatSliderGrp('positionRandomizer_UIctrl', value=True, query=True)

    translateControls = True
    rotateControls = False
    handleRandomizer(translateControls, rotateControls, controlValue)

def randomizeRotationChildControls(*args):
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

def resetMasterControlPositions(*args):
    masterControls = cmds.ls("*MASTER*",transforms=True)

    # reset positions of X, Y, Z axes controls ( in later releases )
    # reset the attribute "positionMultiplier" on every singe control
    for item in masterControls:
        for axis in ["X","Y","Z"]:
            cmds.setAttr(item +'.translate'+ axis, 0)

def resetSlaveControlPositions(*args):
    slaveControls = cmds.ls("*SLAVE*",shapes=False,transforms=True)

    for item in slaveControls:
        cmds.setAttr(item +'.positionMultiplier', 1)
