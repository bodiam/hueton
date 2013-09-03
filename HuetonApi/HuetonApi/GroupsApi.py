# Author: Enric Ballo

# GroupsApi Class
# We can have more than one group, and each group have one name and a list of lights
# Example:
# Groups['kitchenGroup','livingRoomGroup'...]
class GroupsApi():
    def __init__(self):
        self.groups = []

    def addGroup(self, groupToAdd):
        self.groups.append(groupToAdd)

    def removeGroup(self, group):
        self.groups.remove(group)

    def addLightToGroup(self, group, lightToAdd):
        isGroup = False
        for i in self.groups:
            if (group == i):
                isGroup = True
                i.addLight(lightToAdd)

        if (isGroup == False):
            print("The Group dosen't exists")

    def removeLightFromGroup(self, group, lightToRemove):
        isGroup = False
        for i in self.groups:
            if (group == i):
                isGroup = True
                i.removeLight(lightToRemove)

        if (isGroup == False):
            print("The Group dosen't exists")

    def getTotalLightsForGroup(self, group):
        isGroup = False
        total = 0
        for i in self.groups:
            if (group == i):
                isGroup = True
                total = i.get_all_lights()

        if (isGroup == False):
            print("The Group dosen't exists")

        return total

    def get_all_groups(self):
        for i in self.groups:
            print(i.printDetails())
        return len(self.groups)

# Group Class
# Example:
# kitchen (lamp1, lamp2, lamp3)        
class Group():
    def __init__(self, name):
        self.name = name
        self.listOfLights = []

    def changeNameGroup(self, newName):
        self.name = newName

    def addLight(self, light):
        self.listOfLights.append(light)

    def removeLight(self, light):
        self.listOfLights.remove(light)

    def get_all_lights(self):
        return len(self.listOfLights)

    def printDetails(self):
        print("Name : " + self.name)
        count = 0
        for i in self.listOfLights:
            print(str(count) + " - Light " + i)
