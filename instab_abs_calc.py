
from typing import Set
import javalang
import os
import fnmatch


classesCount =0
matches = []
packageSet=set()

classArray=[]
classDependenciesArray=[]

direct=input("Enter full path of directory containing package (preferably without tests): ")

choicePackage=input("Enter name package to get abstractness and instability : ")
print(direct)

for root, dirnames, filenames in os.walk(direct):
    if "test" in root:
        continue
    else:
        for filename in fnmatch.filter(filenames, '*.java'):
            matches.append(os.path.join(root, filename))

#Get all different class names and their packages 
for path in matches:
    with open(path) as f:
        tree = javalang.parse.parse(f.read())
        packageSet.add(tree.package.name)
        clDec=tree.filter(javalang.tree.ClassDeclaration)

        try:
            classData = next(clDec)
        except StopIteration:
            interDec=tree.filter(javalang.tree.InterfaceDeclaration)
            classData = next(interDec)
            # continue



        classArray.append([tree.package.name,classData[1].name])

        

#Add dependencies of class to array
for path in matches:
    with open(path) as f:
        tree = javalang.parse.parse(f.read())

        tempSet=set()
        
        clDec=tree.filter(javalang.tree.ClassDeclaration)

        try:
            classData = next(clDec)
        except StopIteration:
            interDec=tree.filter(javalang.tree.InterfaceDeclaration)
            classData = next(interDec)

        memberRef=tree.filter(javalang.tree.MemberReference)

        classCreate=tree.filter(javalang.tree.ReferenceType)
    

    for members in memberRef:
        for cList in classArray:
            tempPackage=""
            flag=0
            if cList[1]==members[1].qualifier:
                tempPackage=cList[0]
                flag=1

            if members[1].qualifier != '' and members[1].qualifier != None and (tempPackage!=tree.package.name and flag==1):
                tempSet.add(members[1].qualifier)
                

    for newlyClass in classCreate:
        for cList in classArray:
            if cList[1]==newlyClass[1].name:
                tempPackage=cList[0]
            # Check if Depedant Class is a user created one  and 
            if newlyClass[1].name == cList[1] and tempPackage!=tree.package.name:
                tempSet.add(newlyClass[1].name)


    

    classDependenciesArray.append([tree.package.name,classData[1].name,tempSet])


finalList=[]

#Add Fan-in Classes (even a class going to more than one class in the same package)
for nClass in classDependenciesArray:
    newSet=set()
    for nSets in classDependenciesArray:
        if nClass[1] in nSets[2]:
            newSet.add(nSets[1])
    finalList.append([nClass[0],nClass[1],nClass[2],newSet])

#finalList contains all classes with their outgoing and ingoing dependecies
#but there remains a problem, what if there is a class in a package has n (>1) outgoing
#dependecy to different classes in another package .
#Should the Fan-out be n or only count as 1. This program implements the latter


numAbstract=0
numTotal=0

#Calculate number of total number of classes (including abstract classes
# and interfaces) ,abstract classes and interfaces
for path in matches:
    with open(path) as f:
        tree = javalang.parse.parse(f.read())
        thing2=tree.filter(javalang.tree.ClassDeclaration)

        if tree.package.name == choicePackage:
            numTotal=numTotal+1
            try:
                classData = next(thing2)
            except StopIteration:
                numAbstract = numAbstract +1
                continue


            if 'abstract' in classData[1].modifiers:
                numAbstract = numAbstract +1


try:
    print("Abstractness : {}".format(numAbstract/numTotal))
except ZeroDivisionError:
    print("Package does not exist")

#For each class in a chosen package ,get all outgoing dependecies
#If a class has 2 or more outgoing dependencies to the same package ,count it as 1
fanOut=set()
for finalO in finalList:
    if finalO[0]==choicePackage:
        for cL in finalO[2]:
            for classArr in classArray:
                if cL == classArr[1]:
                    fanOut.add((finalO[1],classArr[0]))

#For each class in a chosen package, get all ingoing dependencies
#if a class has 2 more ingoing dependecies to the chosen package, count it as 1
fanIn=set()
for finalI in finalList:
    if finalI[0]==choicePackage:
        for cL in finalI[3]:
            for classArr in classArray:
                if cL == classArr[1]:
                    fanIn.add((cL,classArr[0]))



try:
    print("Instability : {}".format(len(fanOut)/(len(fanOut)+len(fanIn))))
except ZeroDivisionError:
    print("This package has no outgoing or ingoing dependencies.")
