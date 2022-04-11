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

attributes = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ']
cmds.setAttr('nurbsSquare1.' + 'translateX', position[0])
cmds.setAttr('nurbsSquare1.' + 'translateY', position[1])
cmds.setAttr('nurbsSquare1.' + 'translateZ', position[2])

cmds.setAttr('nurbsSquare1.' + 'rotateX', rotation[0])
cmds.setAttr('nurbsSquare1.' + 'rotateY', rotation[1])
cmds.setAttr('nurbsSquare1.' + 'rotateZ', rotation[2])

=====
joint_orient = cmds.getAttr('{}.jointOrient'.format(joint_name))[0]
world_rotation = cmds.xform(joint_name, q=True, worldSpace=True, rotation=True)
cmds.setAttr('{}.jointOrient'.format(joint_name), 0, 0, 0)
cmds.xform(joint_name, worldSpace=True, rotation=world_rotation)
