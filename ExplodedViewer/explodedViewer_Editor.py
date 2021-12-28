import random

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
            return

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

# UI here

windowWidth = 256

cmds.window("Exploded Viewer",width=windowWidth)

cmds.frameLayout( label='Modify Controls')
cmds.text( label='', align="left" )
cmds.text( label='Randomize control positions', align="left" )
cmds.floatSliderGrp('positionRandomizer_UIctrl', field=True, minValue=-0.0, maxValue=10.0, fieldMinValue=0.0, fieldMaxValue=10.0, value=0, changeCommand=randomizeChildControls, width=windowWidth )
#cmds.text( label='Randomize axes', align="left" )
cmds.text( label='', align="left" )
cmds.text( label='Randomize control rotations', align="left" )
cmds.floatSliderGrp('rotationRandomizer_UIctrl', field=True, minValue=-0.0, maxValue=360.0, fieldMinValue=0.0, fieldMaxValue=360.0, value=0, changeCommand=randomizeRotationChildControls, width=windowWidth )
cmds.separator()
cmds.button(width=windowWidth, label="Reset Parent Control Positions", align="left", command=resetMasterControlPositions)
cmds.button(width=windowWidth, label="Reset Child Control Positions", align="right", command=resetSlaveControlPositions)
cmds.text( label='', align="left" )

cmds.showWindow()
