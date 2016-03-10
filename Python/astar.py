class node():

    def __init__(self,x,y,name="unnamed"):
        
        self.x = x
        self.y = y
        self.h = 0
        self.cf = self
        self.n = name

    def calcH(self,goal):

        self.h = ((self.x-goal.x)**2+(self.y-goal.y)**2)**0.5

def aStar(nodeDict,start,goal): 

    for n in nodeDict:
        if n != goal:
            n.calcH(goal)

    openDict = {start:nodeDict[start]}
    closedDict = dict()

    start.g = 0
    start.f = start.h
    
    while len(openDict) != 0:

        for node in openDict:

            current = node

            continue

        for node in openDict:

            if node.f < current.f:

                current = node

        if current == goal:

             finalList = list()

             while current != start:

                  finalList.append(current.n)
                  current = current.cf

             finalList.append(start.n)

             return finalList

        openDict.pop(current,None)
        closedDict[current]=nodeDict[current]

        for adj in closedDict[current]:

            if adj in closedDict:

                continue

            newG = current.g + ((current.x-adj.x)**2+(current.y-adj.y)**2)**0.5

            if adj not in openDict:

                openDict[adj] = nodeDict[adj]

            elif newG >= adj.g:

                continue

            adj.cf = current

            adj.g = newG

            adj.f = adj.g + adj.h

    return False



    

    

    
    


    
    

    

        

        
    
