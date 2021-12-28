# this code can be copied directly into Maya
import maya.cmds as cmds
import random

# new functions
def handleWarning(warningText):
    #cmds.popupMenu(label="foo")
    print warningText

def addNamePrefix():
    controlNamePrefix = cmds.textField('controlNamePrefix', text=True, query=True)
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

    masterControl, namePrefix = createMasterControlShape()

    # if there are groups and user set the option "create sub assemblies for each group", loop through groups, if there are no groups, create one master control for the whole selection
    if createdControl['subAssemblies_created'] == True:
        groupArray = []
        groupChildren = []

        nonGroupArray = []

        for obj in sel:
            #if object has shape children, add master control. If object has slave children, add secondary co
            parentObj = cmds.listRelatives(obj, parent=True)
            if parentObj: groupArray.append(parentObj)
            else: nonGroupArray.append(obj)
            #if parentObj.len > 1: groupArray.append(parentObj)
            #getGroups2 = cmds.ls(sel, geometry = False)
            #if there are groups, create a master control for that group and slave control for children of that group

        #join two arrays
        #remove duplicate selections
        cleanGroupArray = []
        for i in groupArray:
            if i not in cleanGroupArray:
                cleanGroupArray.append(i)

        groupMasterPrefix = "groupMaster_"
        groupMasterControl = createSlaveControls(masterControl, cleanGroupArray, groupMasterPrefix)

        clean_NON_GroupArray = []
        for i in nonGroupArray:
            if i not in clean_NON_GroupArray:
                clean_NON_GroupArray.append(i)

        createSlaveControls(masterControl, clean_NON_GroupArray, namePrefix)

        """
        #SUB-ASSEMBLIES - work in progress - need to re-arrange nodes for the groups
        for groupObj in cleanGroupArray:
            groupMasterPrefix = "groupMaster"
            groupMasterControl = createSlaveControls(masterControl, groupObj, groupMasterPrefix)

            groupChildren = cmds.listRelatives(groupObj, children=True)
            if groupChildren:
                # the master is the group
                subAssemblyNamePrefix = "_subAssemblyChild"
                createSlaveControls(groupMasterControl, groupChildren, subAssemblyNamePrefix)
        """
    else:
        createSlaveControls(masterControl, sel, namePrefix)

def setSlaveControlPosition(obj):
    useXValue = 0
    useYValue = 0
    useZValue = 0
    multiplyConstraintInputValue = 0.5

    #get bounding box of objects to position the slave control circle
    #get highest Y value of bounding box
    #xform = [xmin ymin zmin xmax ymax zmax]
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

    return slaveControl

createdControl = {
'subAssemblies_created': False
}

controlParameters = {
#NEW control regime
"Master" : {
    "masterColor": random.randint(10,15)
}
}
