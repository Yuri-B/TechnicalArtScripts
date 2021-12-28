# this code can be copied directly into Maya
import maya.cmds as cmds
sys.path.append("//Users/yuri/Documents/maya/Maya-Projects/default/scripts/ExplodedViewer");


def resetMasterControlPositions(*args)
    import editor

def randomizeRotationChildControls(*args)
    import editor


def resetMasterControlPositions(*args)
    import editor


def resetSlaveControlPositions(*args)
    import editor

# UI here

windowWidth = 256

cmds.window("Exploded Viewer",width=windowWidth)

tabs = cmds.tabLayout(innerMarginWidth=8, innerMarginHeight=8)

child1 = cmds.rowColumnLayout( numberOfColumns=1 )
cmds.text( label='', align="left" )
cmds.text( label='Control Name Prefix', align="left" )
cmds.textField('controlNamePrefix', editable=True, text='', width=windowWidth)
cmds.text( label='', align="left" )
cmds.checkBox('option_subAssemblies', label='Create Controls for Groups', width=windowWidth, onCommand=ExplodedViewer_Creator.create_subAssemblies, offCommand=ExplodedViewer_Creator.cancel_subAssemblies,  editable=True, value=False)
cmds.text( label='', align="left" )
# backgroundColor=[0,0.3,0.5],
cmds.button(width=windowWidth, label="Create Exploded View Controls", align="left", command=ExplodedViewer_Creator.createMasterControls)
cmds.text( label='', align="left" )
cmds.setParent( '..' )

child2 = cmds.rowColumnLayout( numberOfColumns=1 )
cmds.text( label='', align="left" )
cmds.text( label='Randomize control positions', align="left" )
cmds.floatSliderGrp('positionRandomizer_UIctrl', field=True, minValue=-0.0, maxValue=10.0, fieldMinValue=0.0, fieldMaxValue=10.0, value=0, changeCommand=ExplodedViewer_Editor.randomizeChildControls, width=windowWidth )
#cmds.text( label='Randomize axes', align="left" )
cmds.text( label='', align="left" )
cmds.text( label='Randomize control rotations', align="left" )
cmds.floatSliderGrp('rotationRandomizer_UIctrl', field=True, minValue=-0.0, maxValue=360.0, fieldMinValue=0.0, fieldMaxValue=360.0, value=0, changeCommand=ExplodedViewer_Editor.randomizeRotationChildControls, width=windowWidth )
cmds.separator()
cmds.button(width=windowWidth, label="Reset Parent Control Positions", align="left", command=ExplodedViewer_Editor.resetMasterControlPositions)
cmds.button(width=windowWidth, label="Reset Child Control Positions", align="right", command=ExplodedViewer_Editor.resetSlaveControlPositions)
cmds.text( label='', align="left" )
cmds.setParent( '..' )

cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Create New Controls'), (child2, 'Edit Controls')), width=windowWidth )


cmds.showWindow()
