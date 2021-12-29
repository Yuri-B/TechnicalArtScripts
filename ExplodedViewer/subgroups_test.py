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
