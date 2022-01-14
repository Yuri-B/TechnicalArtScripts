"""
Eric Pavey - 2008-12-19
For the selected hierarchies, zero the joint orient values
on all leaf joints
"""
# Python code
import maya.cmds as mc

kids = mc.listRelatives(mc.ls(selection=True), children=True, type="joint", allDescendents=True)
for k in kids:
    if mc.listRelatives(k, children=True, type="joint") is None:
        for attr in [".jointOrientX", ".jointOrientY", ".jointOrientZ"]:
            mc.setAttr(k+attr, 0)
        print "Zeroed '" + k + ".jointOrient'"

==========

selection = cmds.ls(selection=True)
rotation = cmds.joint(selection, query=True, orientation=True)
position = cmds.joint(selection, query=True, position=True)

NExt orientation

# set joint orientation of end joint based on orientation from previous one
selection = cmds.ls(selection=True)
rotation = cmds.joint(selection, query=True, orientation=True)
position = cmds.joint(selection, query=True, position=True)

cmds.setAttr("nurbsSquare1",translateX = position[0], translateY=position[1], translateZ=position[2], rotateX= rotation[0], rotateY=rotation[1], rotateZ=rotation[2])
