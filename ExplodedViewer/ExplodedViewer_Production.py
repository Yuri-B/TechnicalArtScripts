# this code can be copied directly into Maya

import random

def chooseX_Axis(*args):
    createdControl['axisDirection'] = "X"

def chooseY_Axis(*args):
    createdControl['axisDirection'] = "Y"

def chooseZ_Axis(*args):
    createdControl['axisDirection'] = "Z"

# new functions
def create_subAssemblies(*args):
    print "HEY - created"
    createdControl['subAssemblies_created'] = True

def cancel_subAssemblies(*args):
    print "HEY - not created"
    createdControl['subAssemblies_created'] = False

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

def handleWarning(warningText):
    #cmds.popupMenu(label="foo")
    print warningText

def addNamePrefix():
    controlNamePrefix = cmds.textFieldGrp('controlNamePrefix', text=True, query=True)
    return controlNamePrefix

def createMasterControlShape():
    axisParameters = controlParameters["Master"]
    namePrefix = addNamePrefix()
    masterControlName = namePrefix + "Exploder_Ctrl_MASTER"
    masterControl = cmds.polyCube(name=masterControlName, w=1, h=1, d=1)[0]
    cmds.setAttr(masterControl + ".overrideEnabled", 1)
    cmds.setAttr(masterControl + ".overrideColor", axisParameters["masterColor"])
    #make master controls into boxes
    cmds.setAttr(masterControl + ".overrideLevelOfDetail", 1)

    return masterControl, namePrefix

def createMasterControls(*args):
    # when I will create a way of getting a list of objects, sorting them
    sel = cmds.ls(selection = True, transforms=True)
    if len(sel) < 1:
        handleWarning(warningText="WARNING: please select an object")
        return

    # if there are groups and user set the option "create sub assemblies for each group", loop through groups, if there are no groups, create one master control for the whole selection
    if createdControl['subAssemblies_created'] == True:
        getGroups = cmds.ls(sel, transforms = True)
        print getGroups

        #for obj in sel:
            # if there are groups, create a master control for that group and slave control for children of that group
    else:
        masterControl, namePrefix = createMasterControlShape()
        createSlaveControls(masterControl, sel, namePrefix)

def setSlaveControlPosition(obj):
    useXValue = 0
    useYValue = 0
    useZValue = 0
    multiplyConstraintInputValue = 0.5

    #get bounding box of objects to position the slave control circle
    #get highest Y value of bounding box
    # xform = [xmin ymin zmin xmax ymax zmax]
    objectBoundingBox = cmds.xform(obj, query=True, boundingBox=True, worldSpace=True)

    #if the object's center is placed in negative quadrant, use min, if placed in positive quadrant, use max
    useXValue = (objectBoundingBox[0] + objectBoundingBox[3])/2
    useYValue = (objectBoundingBox[1] + objectBoundingBox[4])/2
    useZValue = (objectBoundingBox[2] + objectBoundingBox[5])/2

    return [useXValue,useYValue,useZValue]

def createMultiplyNodes(selCounter, controlPosition,masterControl,slaveControl):

    # this is the multiply node that allows user to tweak position of slave control. It is connected from slave control's positionMultiplier attribute to other multiply constraint's input 2Y
    addNode = cmds.createNode("plusMinusAverage", name="additionNode_Slave" + str(selCounter))
    cmds.connectAttr(masterControl + ".translate", addNode + ".input3D[0]")
    multiplyNodeMain = cmds.createNode("multiplyDivide", name="multiplicationNode_Slave" + str(selCounter))
    cmds.connectAttr(addNode + ".output3D", multiplyNodeMain + ".input1")

    for axisName in ["X","Y","Z"]:
        cmds.connectAttr(slaveControl + ".positionMultiplier", multiplyNodeMain + ".input2" + axisName )

    cmds.connectAttr(multiplyNodeMain + ".output", slaveControl + ".translate")

def createSlaveControls(masterControl, sel, namePrefix):
    selCounter = 0

    for obj in sel:
        selCounter += 1

        slaveControlNameFull = namePrefix + "Exploder_Ctrl_SLAVE_" + str(selCounter)
        controlPosition = setSlaveControlPosition(obj)

        slaveControl = cmds.polyCube(name=slaveControlNameFull, w=0.5, h=0.5, d=0.5)[0]
        cmds.setAttr(slaveControl + ".translateX", controlPosition[0])
        cmds.setAttr(slaveControl + ".translateY", controlPosition[1])
        cmds.setAttr(slaveControl + ".translateZ", controlPosition[2])

        cmds.setAttr(slaveControl + ".overrideEnabled", 1)
        cmds.setAttr(slaveControl + ".overrideColor", 12)
        #make master controls into boxes
        cmds.setAttr(slaveControl + ".overrideLevelOfDetail", 1)

        cmds.parent(slaveControl,masterControl)
        #parent slave control to object with a constraint ( user can modify weight of constraint)
        cmds.parentConstraint(slaveControl,obj, maintainOffset = True)

        cmds.addAttr(slaveControl, longName="positionMultiplier", attributeType="double", min=-10, max=10, defaultValue=1)
        cmds.setAttr(slaveControl + ".positionMultiplier", edit=True, keyable=True)

        #freeze transformations of slave Controls
        cmds.makeIdentity(slaveControl, apply=True, translate=True, rotate=True, scale=True)

        #general formula for movement: Default bounding box position of slave control ( slightly rounded to 2 decimal places - controlPosition[3]) * positionMultiplier attribute of slave control  * X/Y or Z axis translate coordinate of master control
        # create one node for each slave control; custom attribute * translateY of it helps user to tweak position of the control
        #this is the multiply node that multiplies master control's X, Y or Z translate coord by slave's bounding box corresponding X, Y, Or Z axis transform coord
        createMultiplyNodes(selCounter, controlPosition, masterControl, slaveControl)

def randomizeChildControls(*args):
    randomizerSliderValue = cmds.floatSliderGrp('positionRandomizer_UIctrl', value=True, query=True)

    slaveControls = cmds.ls("*SLAVE*",transforms=True)
    if len(slaveControls) < 1:
        handleWarning(warningText="please create Slave controls")
        return

    minRandValue = (randomizerSliderValue * -1) / 10 + 1
    maxRandValue = randomizerSliderValue

    for item in slaveControls:
        # create a random slider value for each different control
        enterRandomValue = random.uniform(minRandValue,maxRandValue)

        cmds.setAttr(item +'.positionMultiplier', enterRandomValue)

createdControl = {
'subAssemblies_created': False
}

controlParameters = {
#NEW control regime
"Master" : {
    "masterColor": random.randint(10,15),
    "defaultCoordinate": 1
}
}

# UI here

windowWidth = 520

cmds.window("Exploded Viewer",width=windowWidth, height=windowWidth)

cmds.frameLayout( label='Create New Controls' )
cmds.text( label='Step 1: select objects to shift', align="left", height=20)
cmds.text( label='Step 2: Turn on this checkbox to create sub-assemblies for all groups', align="left", height=20)
#cmds.checkBoxGrp('option_chooseAxis', width=windowWidth, labelArray3=['Create Sub-Assemblies for Groups'], onCommand1=chooseX_Axis, onCommand2=chooseY_Axis, onCommand3=chooseZ_Axis, numberOfRadioButtons=3, editable=True, height=20, select=0 )
cmds.checkBox('option_subAssemblies', label='Create Sub-Assemblies for Groups', width=windowWidth, onCommand=create_subAssemblies, offCommand=cancel_subAssemblies,  editable=True, height=20, value=False)

cmds.textFieldGrp('controlNamePrefix', label='Custom name prefix', editable=True, width=windowWidth, text='')
cmds.setParent( '..' )

cmds.rowLayout(height=60, numberOfColumns=2, width=windowWidth)
cmds.button(width=windowWidth - 60, label="Create Exploded View Controls", backgroundColor=[0,0.3,0.5], align="left", command=createMasterControls)
cmds.setParent( '..' )

cmds.frameLayout( label='Advanced Options', collapsable=True, width=windowWidth )
cmds.text( label='Randomize control positions: set randomness multiplier', height=30, align="left" )
cmds.floatSliderGrp('positionRandomizer_UIctrl', field=True, minValue=-0.0, maxValue=10.0, fieldMinValue=0.0, fieldMaxValue=10.0, value=0, changeCommand=randomizeChildControls, height=50 )
#cmds.text( label='Randomize axes', align="left" )
cmds.setParent( '..' )

cmds.frameLayout( label='Reset Existing Controls', collapsable=True )
cmds.rowLayout(height=40, numberOfColumns=2, width=windowWidth)
cmds.button(width=windowWidth/2 - 30, label="Reset Parent Control Positions", align="left", backgroundColor=[0.5,0,0.1], command=resetMasterControlPositions)
cmds.button(width=windowWidth/2 - 30, label="Reset Child Control Positions", align="right", backgroundColor=[0.5,0.5,0], command=resetSlaveControlPositions)
cmds.setParent( '..' )
cmds.setParent( '..' )

cmds.frameLayout( label='Help', collapsable=True )
cmds.text( label='Master Control is the main control for creating exploded view of an assembly of objects. It moves all slave controls that are parented to it, away from itself. The more a Master control is moved along a certain axis, the further slave controls move away from it.', align="left", wordWrap=True, width=windowWidth)
cmds.text( label='Slave Control is the secondary control for creating exploded views. It is used to control each individual object', align="left", wordWrap=True, width=windowWidth )
cmds.text( label='Each slave control has an additional attribute called "Position Multiplier". This attribute adjusts the distance between the master control and slave control. The higher the value, the larger the distance', align="left", wordWrap=True, width=windowWidth )
cmds.setParent( '..' )

cmds.showWindow()
