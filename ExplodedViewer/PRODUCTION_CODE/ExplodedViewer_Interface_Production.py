# this code can be copied directly into Maya
import maya.cmds as cmds
import sys
# ()()()() INSERT YOUR WORKING MAYA SCRIPTS DIRECTORY HERE ()()()()
sys.path.append( '/Users/yuri/Documents/maya/Maya-Projects/tech_art/scripts' )

# CONTROLLER

# editor functions
import editor
def randomizeChildControls(*args):
    editor.randomizeChildControls()

def randomizeRotationChildControls(*args):
    editor.randomizeRotationChildControls()

def resetControlPositions(*args):
    editor.resetControlPositions()

def resetControlRotations(*args):
    editor.resetControlRotations()

def proportionalTranslateControls(*args):
    editor.proportionalControls()

# creator functions
import creator
def createMasterControls(*args):
    creator.createMasterControls()

def create_subAssemblies(*args):
    creator.create_subAssemblies()

def cancel_subAssemblies(*args):
    creator.cancel_subAssemblies()

# VIEW with UI here

windowWidth = 256

cmds.window("Exploded Viewer",width=windowWidth)

tabs = cmds.tabLayout(innerMarginWidth=8, innerMarginHeight=8)

child1 = cmds.rowColumnLayout( numberOfColumns=1 )
cmds.text( label='', align="left" )
cmds.text( label='Create Control Name Prefix', align="left" )
cmds.textField('controlNamePrefix', editable=True, text='', width=windowWidth)
cmds.text( label='', align="left" )
# backgroundColor=[0,0.3,0.5],
cmds.button(width=windowWidth, label="Create Exploded View Controls", align="left", command=createMasterControls)
cmds.text( label='', align="left" )
cmds.setParent( '..' )

child2 = cmds.rowColumnLayout( numberOfColumns=1 )
cmds.text( label='', align="left" )
cmds.text( label='Child Controls', align="left" )
cmds.text( label='', align="left" )
cmds.text( label='Randomize positions', align="left" )
cmds.floatSliderGrp('positionRandomizer_UIctrl', field=True, minValue=-0.0, maxValue=10.0, fieldMinValue=0.0, fieldMaxValue=10.0, value=0, changeCommand=randomizeChildControls, width=windowWidth )
cmds.text( label='Translate child controls proportionally', align="left" )
cmds.floatSliderGrp('proportionalTranslate_UIctrl', field=True, minValue=-0.0, maxValue=10.0, fieldMinValue=0.0, fieldMaxValue=10.0, value=0, changeCommand=proportionalTranslateControls, width=windowWidth )
cmds.separator()
#cmds.text( label='Randomize axes', align="left" )
cmds.text( label='', align="left" )
cmds.text( label='Randomize control rotations', align="left" )
cmds.floatSliderGrp('rotationRandomizer_UIctrl', field=True, minValue=-0.0, maxValue=360.0, fieldMinValue=0.0, fieldMaxValue=360.0, value=0, changeCommand=randomizeRotationChildControls, width=windowWidth )
cmds.text( label='', align="left" )
cmds.separator()
cmds.button(width=windowWidth, label="Reset Positions", align="left", command=resetControlPositions)
cmds.button(width=windowWidth, label="Reset Rotations", align="right", command=resetControlRotations)
cmds.text( label='', align="left" )
cmds.setParent( '..' )

cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Create New Controls'), (child2, 'Edit Controls')), width=windowWidth )

cmds.showWindow()
