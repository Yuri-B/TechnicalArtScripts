import maya.cmds as cmds

joints = cmds.ls(selection=True, type='joint')
for j in joints:
    #select an FK joint. Parent constraint it to SKN joints
    print j

    truncatedJointName = j[3:]
    skinJointName = "SKN_" + truncatedJointName
    #optionally parent a corresponding IK joint as well
    ikJointName = "IK_" + truncatedJointName
    #get corresponding SKN joint
    #test parenting
    #cube = cmds.polyCube()[0]
    cmds.parentConstraint( j, ikJointName, skinJointName, maintainOffset=True )
    #select IK joint. Parent constraint it to SKN joints

print len(joints)


#select all joints with name prefix "IK_jnt" ; parent constraint them to all joints named "SKN_jnt"
cmds.parentConstraint( 'cone1', 'cube1', maintainOffset=false )
