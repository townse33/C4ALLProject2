import pygame
import time
from random import *
import math
import menuv2
import os
import sys
from astar import *

pygame.mixer.pre_init(44100,16,2,4096)#Background Music
pygame.init()

#Background Music
pygame.mixer.music.load("backgroundsongofchoice.mp3")#As you probably know song should be in the game folder
pygame.mixer.music.set_volume(0)#Volume
pygame.mixer.music.play(-1)#This loops the song

nList = False

#Colour palette 
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
pblue = (0,0,255)

done = False
mineShow = False
mineText = "Sell or refuel here!"
#Muted colours for inventory items
invred = (195,60,60)
invyellow = (190,210,110)
invgreen = (105,185,130)
invblue = (135,206,250)
invSize = 0
invNote = False
shopNote = False

mode="Player"

fuel = 100
texFuel = 100

mineArg = [0,0,0,0]

timeR = 0
timeR2 = 0
timeN = 0
timeF = 0
timeF2 = 0

gCredits = 0

#Window dimensions; resolution
display_width = 1200
display_height = 800

winMode = pygame.DOUBLEBUF | pygame.HWSURFACE #| pygame.FULLSCREEN #Enable hardware acceleration, remove first comment for fullscreen

gameDisplay = pygame.display.set_mode((display_width, display_height),winMode) #Initialise pygame window

#Title and caption
pygame.display.set_caption("C4 ALL Project 2")

#Time Variables, initialise FPS clock
FPS = 150 #One frame = Ten milliseconds
clock = pygame.time.Clock()

#Universe stores all object information, inMemory determines what to load
universe = []
inMemory = []
memLimit = 6 #How many objects to leave in memory

texX = 0 #Player X position variable for text, for controlled updating
texY = 0 #Player Y position for text
texSpeed = 0 #Player speed for text

#Inventory setup
itemCost = {"nebulium":39, "bismuth":81, "polonium":56, "francium":93} # Costs of all the items that can be collected
# nebulium == yellow, bismuth == red, polonium == green, francium == blue

printList = ["nebulium", "bismuth", "polonium", "francium"] # Used to print total collected items at end
inventory = ["nebulium", "bismuth", "polonium", "francium"] # Inventory items collected by the user
itemAmount = {"nebulium":0, "bismuth":0, "polonium":0, "francium":0} #How much of each item the user has

money = 0 # Credits owned by the user
alphaOrNumeric = True   #True indicates alphabetic, False indicates Numeric
totalItems = {"nebulium":0, "bismuth":0, "polonium":0, "francium":0} #Total amount of items collected by user, cumulative

idCounter = 0

multi = 1

def addToInventory(modList, item):
    """Not used but could still be implemented"""
    modList.append(item)

def sellInventory(modList, money):
    global invSize, gCredits, multi
    """ Will output the amount of money gained from selling all the items
    as well as removing all the items sold from the inventory """

    gCredits = 0
    
    for i in modList: # Adds money, using the itemCost dictionary
        money += itemCost[ i ] * itemAmount[ i ] * multi
        gCredits += itemCost[ i ] * itemAmount[ i ] * multi
        
    itemAmount["nebulium"] = 0 #Defaults the dictionary amounts to 0, removing them from the inventory
    itemAmount["bismuth"] = 0
    itemAmount["polonium"] = 0
    itemAmount["francium"] = 0

    invSize = 0
    
    return(money)

    # Found that iterating over the list caused a problem with List Aliasing
    # and removing items from the list being iterated over

def mine(n,b,p,f):

    global inventory, invSize

    invSize = 0

    for mineral in itemAmount:

        invSize += itemAmount[mineral]
    
    if invSize < 20:

            neb = randint(0,n)
            bis = randint(0,b)
            pol = randint(0,p)
            fra = randint(0,f)

            itemAmount["nebulium"] += neb
            itemAmount["bismuth"] += bis
            itemAmount["polonium"] += pol
            itemAmount["francium"] += fra

            totalItems["nebulium"] += neb
            totalItems["bismuth"] += bis
            totalItems["polonium"] += pol
            totalItems["francium"] += fra

            invSize = 0

            for mineral in itemAmount:

                invSize += itemAmount[mineral]

            while invSize > 20:

                ranMat = choice(inventory)

                if itemAmount[ranMat] > 0:

                    itemAmount[ranMat] -= 1

                invSize = 0

                for mineral in itemAmount:

                    invSize += itemAmount[mineral]

def mergeSort(sortList):
    """ Will order the items of any imported list alphabetically, in ascending order"""

    if len(sortList)>1:
        middle = len(sortList) // 2
        left = sortList[:middle]
        right = sortList[middle:]

        mergeSort(left)
        mergeSort(right)

        a = 0
        b = 0
        c = 0
        while a < len(left) and b < len(right):
            if left[a] < right[b]:
                sortList[c]=left[a]
                a += 1
            else:
                sortList[c]=right[b]
                b += 1
            c += 1

        while a < len(left):
            sortList[c]=left[a]
            a += 1
            c += 1

        while b < len(right):
            sortList[c]=right[b]
            b += 1
            c += 1

def bubbleSort(sortList):
    """ Will order the items of any imported list alphabetically, in ascending order"""
    
    for i in range(len(sortList)):
        for j in range(len(sortList)-1-i):
            if itemAmount[ sortList[j] ] > itemAmount[ sortList[j + 1] ]:
                sortList[j], sortList[j+1] = sortList[j+1], sortList[j]

def binarySearch(searchValue, array):
    """ Not used, however could be implemented later"""
    first = 0
    last = len(array) - 1
    beenFound = False
	
    while first <= last and not beenFound:
        midpoint = (first + last)//2

        if array[midpoint] == searchValue:
            result = str(searchValue) + " has been found"
            beenFound = True
            
	    
        else:
            if searchValue < array[midpoint]:
                last = midpoint-1
            else:
                first = midpoint+1	
    return()

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

#Class System
class Ship:
        """This class deals with player controlled movement"""

        def __init__(self, display_width, display_height):

            Ship = pygame.image.load("spaceship.png") #Load the sprite image
            
            self.dir = 0 #Direction of ship in degrees, taken from a north bearing
            self.rot = 0 #Current rotation amount
            self.posX = 0 #X position of player on map
            self.posY = 0 #Y position of player on map
            self.accX = 0 #X acceleration of player
            self.accY = 0 #Y acceleration of player
            self.dW = display_width #Screen width
            self.dH = display_height #Screen height

            self.adv = False #Is ship accelerating?
            self.decc = False
            

            #store ship image dimensions
            self.sW, self.sH = Ship.get_size()

            #centre ship by subtracting half ship size from given dimensions
            gameDisplay.blit(Ship, (self.dW/2-self.sW*0.5,self.dH/2-self.sH*0.5))

        def update(self):
            global display_height, display_width, fuel

            #Modulo on direction to prevent direction exeeding 360 degrees
            self.dir = self.dir % 360
            #Increment direction by rotation amount
            self.dir += self.rot
            
            if self.adv == True:
                
                self.accX -= math.sin(math.radians(self.dir))*0.02 #Sine rule to find change in player X acceleration
                self.accY -= math.sin(math.radians(90-self.dir))*0.02 #Sine rule to find change in player Y acceleration

                fuel -= 0.15

            if self.decc == True:

                self.accX = self.accX*0.99
                self.accY = self.accY*0.99

            #Rotate ship to current direction
            Ship = pygame.transform.rotate(pygame.image.load("spaceship.png"),self.dir)

            spriteW, spriteH = Ship.get_size()

            gameDisplay.blit(Ship, (display_width/2-spriteW*0.5,display_height/2-spriteH*0.5))

            self.posX +=self.accX
            self.posY -=self.accY

        def rotL(self):
            self.rot = 1 #Rotate anticlockwise 1 degree per frame
        def rotR(self):
            self.rot = -1 #Rotate clockwise 1 degree per frame
            
        def fwd(self):
            self.adv = True

        def bwd(self):
            self.decc = True

        """def reload(self):
            Ship = pygame.image.load("spaceship.png") #Load the sprite image
            self.dW = display_width #Screen width
            self.dH = display_height #Screen height
            
            #centre ship by subtracting half ship size from given dimensions
            gameDisplay.blit(Ship, (self.dW/2-self.sW*0.5,self.dH/2-self.sH*0.5))"""

            
class NotAShip:
    """Placeholder class used for objects that are not the player, i.e. ones that need scrolling"""

    def __init__(self, posX, posY, img, N=0,B=0,P=0,F=0,shop=False):

        global universe, inMemory, idCounter

        Object = pygame.image.load("planets/" + img) #This time, we take an image as a string as a parameter too

        self.sW, self.sH = Object.get_size()

        self.posX = posX
        self.posY = posY
        self.disX = posX + self.sW/2  #Centering only affects an object's initial screen position so this is done before the blit, multipliers to compensate for pygame's bad centering
        self.disY = posY + self.sH /2

        
        self.img = "planets/" + img #We maintain the image path as an attribute so it need only be provided once
        self.n = N
        self.b = B
        self.p = P
        self.f = F
        self.inMem = False #Planet does not start in memory
        self.id = idCounter

        idCounter +=1

        self.shop = shop

        gameDisplay.blit(Object, (self.disX,self.disY))

        universe.append(self)
    
    def update(self,toBlit):

        global mineShow,display_width,display_height,money,fuel,mineArg,shopNote,invNote,invSize

        if not(toBlit):

            self.disX -= player.accX #Evaluate difference in object to player position on the screen
            self.disY -= player.accY

        if toBlit:
            
            Object = pygame.image.load(self.img)

            pygame.Surface.convert(Object)

            gameDisplay.blit(Object, (math.floor(self.disX+self.sW/3),math.floor(self.disY+self.sH/3))) #We use floor division as we cannot have fractional pixels

            if abs(self.disX+self.sW/2-display_width/2) < 150 and abs(self.disY+self.sH/2-display_height/2) < 150:

                mineShow = True
                fuel = 100

                if self.shop:

                    mineArg = [0,0,0,0]

                    if invSize>0:
                        money = sellInventory(inventory,money)
                        invNote = True
                        

                    shopNote = True

                else:

                    mineArg = [self.n,self.b,self.p,self.f]
                    shopNote = False
                    invNote = False
                    

def ranValue():
    global inventory, itemCost
    for item in inventory:
        itemCost[item] = randint(10,100)
    
#Game states
gameExit = False
gameOver = False

#init player
player = Ship(display_width/2, display_height/2)

#Object1 = NotAShip(0, 0,"earth.jpg",0,0,0,0,True) #Places aobject
#Object2 = NotAShip(600,600,"moon.jpg",1) #Places a Moon object

fullscreenStat = False

multiEnable = False



def secGen(startW,endW,startH,endH,planetNo,spread):
    
    global planetID

    testList = list()

    for k in range(planetNo):
    
        ranX = randint(startW,endW)
        ranY = randint(startH,endH)

        for planet in testList:

            loop = True

            while loop:

                test1 = planet.posX > ranX - spread
                test2 = planet.posX < ranX + spread

                test3 = planet.posY > ranY - spread
                test4 = planet.posY < ranY + spread

                test5 = ranX > startW + spread
                test6 = ranX < endW - spread

                test7 = ranY > startH + spread
                test8 = ranY < endW - spread
                
                if (test1 and test2) and (test3 and test4):

                    ranX = randint(startW,endW)
                    ranY = randint(startH,endH)

                else:

                    loop = False
                    
        ranImg = choice(os.listdir("Planets/"))

        print(ranImg)

        r1 = randint(0,4)
        r2 = randint(0,4)
        r3 = randint(0,4)
        r4 = randint(0,4)

        sRan = randint(0,4)

        if sRan == 4:

            shopRan = True
            r1=0
            r2=0
            r3=0
            r4=0

        else:

            shopRan = False

        planetID = NotAShip(ranX,ranY,ranImg,r1,r2,r3,r4,shopRan)

        testList.append(planetID)

        print(planetID.id)

uniGraph = dict()
fuelDis = 1000
    
                
def universeGen(uniH,uniW,secPlanets,spread):

    global universe, uniGraph, fuelDis, nodeList
                
    universeH = uniH
    universeW = uniW

    secNo = (universeH * universeW) / (display_height * display_width)

    rowX = -universeW/2 
    colY = -universeH/2

    nodeList = list()

    for column in range(universeH//display_height):
        for row in range(universeW//display_width):
            #if not((column==0 and row==0) or (abs(column)==1 and abs(row)==1)):
                secGen(row*display_width+rowX,(row+1)*display_width+rowX,column*display_height+colY,(column+1)*display_height+colY,secPlanets,spread)
    nodeID = 0
    for planet in universe:

        planetNode = "n" + str(planet.id)

        planetNode = addNode(planetNode,planet.posX,planet.posY,"n" + str(planet.id))

        nodeList.append(planetNode)

    for node in nodeList:

        adjList = list()

        for planet2 in nodeList:

            test = ((planet2.x - node.x)**2+(planet2.y-node.y)**2)**0.5 < fuelDis

            if test:

                adjList.append(planet2)
                
        uniGraph[node] = adjList

def pathFind(target):

    global universe, player, uniGraph, fuelDis, nodeList

    addList = list()

    for planet in universe:

        if abs(planet.disX) < fuelDis and abs(planet.disY) < fuelDis:

            addList.append(nodeList[planet.id])
            
    start = addNode("start",player.posX+1,player.posY+1,"start")

    nodeList.append(start)

    uniGraph[start] = addList

    return aStar(uniGraph,start,nodeList[target])

def automate(nodeL):

    global nodeList, fuel, player, universe, display_height,display_width, prevNode, inventory, money, clock, FPS, mode

    print(nodeL)

    while len(nodeL)> 1:

        currNode = universe[int(nodeL[-2][1:])]

        print(currNode.id,currNode.posX,-currNode.posY)

        targetDir = math.degrees(math.atan2(-currNode.posY-player.posY,currNode.posX-player.posX))-90

        if targetDir < 0:

            targetDir = 360+targetDir

        while int(player.dir) != int(targetDir):

            player.rot = -1

            render()
            cpuEvents()
            if mode == "Player":

                return
            clock.tick(FPS)
        
        player.dir = targetDir

        print(player.dir)
        print(targetDir)

        render()

        player.rot=0

        loop = True

        player.adv = True

        while loop:

            dis = ((player.posX-currNode.posX)**2+(player.posY+currNode.posY)**2)**0.5

            targetDir = math.degrees(math.atan2(-currNode.posY-player.posY,currNode.posX-player.posX))-90

            if abs(targetDir-player.dir) > 0.1:

                player.dir = targetDir

            if dis < 50:

                player.adv = False

                player.accX = 0
                player.accY = 0

                loop = False

                fuel = 100

            render()

            cpuEvents()

            if mode == "Player":

                return

            clock.tick(FPS)

        nodeL.pop(-2)

        mine(currNode.n,currNode.b,currNode.p,currNode.f)

        prevNode = currNode.id

        if len(nodeL) == 1:

            money = sellInventory(inventory,money)

            return True

        player.decc = False

universeGen(10000,10000,1,200) #Universe Height, Width, Planet Density Factor, Spread

prevNode = 0

def cpuEvents():
    global mode, display_width, display_height, winMode, gameDisplay, fullscreenStat

    for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
        
                if event.key == pygame.K_e:
                            mode = "Player"
                if event.key == pygame.K_ESCAPE:
                        menuv2.pauseMenu()
                if event.key == pygame.K_p: #P for fullscreen lol
                        
                        if fullscreenStat == True:
                             
                                winMode = pygame.DOUBLEBUF | pygame.HWSURFACE
                                display_width = 1200
                                display_height = 800
                                gameDisplay = pygame.display.set_mode((display_width, display_height),winMode)
                                fullscreenStat = False
                        else:
                           
                                winMode = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN #Set display variable to include fullscreen
                                display_width = 1200
                                display_height = 800
                                gameDisplay = pygame.display.set_mode((display_width, display_height),winMode) #Generate new display fullscreen
                                #player.reload()
                                fullscreenStat = True
        
        #Allows a user to close the window using the close button
            if event.type == pygame.QUIT:
                gameOver = True
            
timeEnd = True

def render():

    global endTime,endMin,endSec,timeStr,timeEnd,mode, prevNode, multi, ranNode, nodeList, nList, winMode, white, red, green, pblue, totalItems, money, black, shopNote, invred, invyellow, invgreen, invblue, gameDisplay, inMemory, memLimit, universe, fuel, display_width, display_height, inventory, texX, texY, texFuel, texSpeed, timeR, timeR2, timeF, timeF2, itemAmount, mineText, mineShow, invSize, invNote, gCredits, printList, alphaOrNumeric, clock, FPS
   
    gameDisplay.fill(black)

    while nList == False:

        ranNode = randint(0,len(nodeList)-1)

        nList = pathFind(ranNode)
        
     
    if len(nList)>1:

        mulX = universe[int(nList[0][1:])].posX
        mulY = -universe[int(nList[0][1:])].posY

        if universe[int(nList[-2][1:])].inMem == False:

            universe[int(nList[-2][1:])].inMem=True
            inMemory.append(universe[int(nList[-2][1:])])
            
    else:

        multi += 1
        nList = False
        mulX = "N/A"
        mulY = ""

    if universe[prevNode].inMem == False:

            universe[prevNode].inMem=True
            inMemory.append(universe[prevNode])

        
    if len(inMemory) > memLimit: #Check if memory limit exceeded, removed earliest entry in memory list if so

               inMemory[0].inMem = False
               inMemory.pop(0)
                    
    for planet in inMemory: #Update all objects in memory
            planet.update(True)

    for planet in universe: #Display any unloaded planet if within distance criteria and is not already in memory
            planet.update(False)
            if (abs(player.posX-planet.posX) < display_width*0.6 and abs(player.posY-planet.posY) < display_height*0.6) and planet.inMem == False:
                    planet.inMem = True
                    inMemory.append(planet)
            

    player.update() #Update player object

    font = pygame.font.Font("trench.otf", 36) #Defines sci-fi font from external file

    #Intentionally slow down text updates, it is very distracting and hard to read when they are updated once per frame
    if pygame.time.get_ticks() % 4 == 0:
            texY = player.posY
            texX = player.posX
            texSpeed = round(40*math.sqrt((player.accX)**2+(player.accY)**2),1)
            if fuel < 0:
                texFuel = 0
            else:
                texFuel = round(fuel,2)
                
    #stat bar
    statBar = pygame.Surface((display_width,36)) #Create a stats GUI bar as a surface
    statBar.set_alpha(200) #Make bar partly transparent                
    statBar.fill((20,50,150)) #Colour bar blue           
    gameDisplay.blit(statBar, (0,display_height-36)) #Render GUI bar at bottom of screen   

    #mergeSort(inventory)

    text = font.render("X: " + str(math.floor(texX)) + "        Y: " + str(math.floor(texY)) + "        Speed: " + str(texSpeed) + "km/s" + "        Credits: " + str(money) + "        Fuel:" + str(texFuel) + "%", 1, (100, 200, 255)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
    textRect.centery = (math.floor(display_height-18))
    gameDisplay.blit(text, textRect)

    #inventory bar
    inventoryBar = pygame.Surface((display_width*0.3,90)) #Create a stats GUI bar as a surface
    inventoryBar.set_alpha(150) #Make bar partly transparent
    inventoryBar.fill((20,50,150)) #Colour bar blue           
    gameDisplay.blit(inventoryBar, (display_width*0.35,5)) #Render GUI bar at top of screen (previous entry said bottom of screen, despite position at top)

    if timeR < 60000:
        timeR = pygame.time.get_ticks() - timeR2
    else:
        timeR2 = pygame.time.get_ticks()
        timeR = 0
        ranValue()
        
    if timeF < 2000:
        timeF = pygame.time.get_ticks() - timeF2
    else:
        timeF2 = pygame.time.get_ticks()
        timeF = 0
        fuel -= 1

    #Item Icons (can replace with sprites later if so desired) future proofed in case of resolution manipulation
    invIcon1 = pygame.draw.polygon(gameDisplay, invyellow, (((display_width/2)-105, 10), ((display_width/2)-130, 35), ((display_width/2)-105, 60), ((display_width/2)-80, 35)))
    invIcon2 = pygame.draw.polygon(gameDisplay, invred, (((display_width/2)-35, 10), ((display_width/2)-60, 35), ((display_width/2)-35, 60), ((display_width/2)-10, 35)))
    invIcon3 = pygame.draw.polygon(gameDisplay, invgreen, (((display_width/2)+35, 10), ((display_width/2)+10, 35), ((display_width/2)+35, 60), ((display_width/2)+60, 35)))
    invIcon4 = pygame.draw.polygon(gameDisplay, invblue, (((display_width/2)+105, 10), ((display_width/2)+80, 35), ((display_width/2)+105, 60), ((display_width/2)+130, 35)))

    i2Text = font.render(str(itemAmount["nebulium"]), 1, (100, 200, 255))
    i2TextRect = i2Text.get_rect()
    i2TextRect.centerx = (int((display_width/2)-105)) #Position text under correct icon
    i2TextRect.centery = (80)
    gameDisplay.blit(i2Text, i2TextRect)

    i1Text = font.render(str(itemAmount["bismuth"]), 1, (100, 200, 255))
    i1TextRect = i1Text.get_rect()
    i1TextRect.centerx = (int((display_width/2)-35)) #Position text under correct icon
    i1TextRect.centery = (80)
    gameDisplay.blit(i1Text, i1TextRect)

    i3Text = font.render(str(itemAmount["polonium"]), 1, (100, 200, 255))
    i3TextRect = i3Text.get_rect()
    i3TextRect.centerx = (int((display_width/2)+35)) #Position text under correct icon
    i3TextRect.centery = (80)
    gameDisplay.blit(i3Text, i3TextRect)

    i4Text = font.render(str(itemAmount["francium"]), 1, (100, 200, 255))
    i4TextRect = i4Text.get_rect()
    i4TextRect.centerx = (int((display_width/2)+105)) #Position text under correct icon
    i4TextRect.centery = (80)
    gameDisplay.blit(i4Text, i4TextRect)

    text = font.render("N      B      P       F", 1, (0,0,0)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.5)) #Position text at top of page in center (previous entry said bottom of screen, despite position at top)
    textRect.centery = (math.floor(35))
    gameDisplay.blit(text, textRect)

    if mode == "Player":

        if mineShow == True:

            noteColour = (200, 160, 80)

            fillColour = (20,50,150)

            showBar = True

            if invSize == 20:

                mineText = "Inventory Full!"
                
            elif invNote == True and gCredits != 0:

                mineText = "Gained " + str(gCredits) + " credits!"

                noteColour = (150,255,150)
                
            elif not shopNote:

                mineText = "Press M to mine"

            else:

                mineText = "Sell minerals here!"
        elif fuel<25:

            mineText = "Warning: Low Fuel!"

            fillColour = (255,50,20)

            noteColour = (200, 160, 80)

            showBar = True

        else:

            showBar = False
    else:

        noteColour = (200, 160, 80)

        fillColour = (20,50,150)

        showBar = True

        mineText = "Pathfinding..."

    if showBar:
        
        mineBar = pygame.Surface((display_width*0.3,45)) 
        mineBar.set_alpha(150) #Make bar partly transparent
        mineBar.fill(fillColour)          
        gameDisplay.blit(mineBar, (display_width*0.35,100)) 

        text = font.render(mineText, 1, noteColour) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(125))
        gameDisplay.blit(text, textRect)
        
    mulBar = pygame.Surface((display_width*0.34,50)) 
    mulBar.set_alpha(150) #Make bar partly transparent
    mulBar.fill((20,50,150))          
    gameDisplay.blit(mulBar, (0,25)) 

    text = font.render("Multiplier at: " + str(mulX) + "," + str(mulY), 1, (100, 200, 255)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.17)) #Position text at bottom of page in center
    textRect.centery = (math.floor(50))
    gameDisplay.blit(text, textRect)

    mul2Bar = pygame.Surface((display_width*0.05,50)) 
    mul2Bar.set_alpha(150) #Make bar partly transparent
    mul2Bar.fill((20,50,150))          
    gameDisplay.blit(mul2Bar, (display_width*0.95,25)) 

    text = font.render(str(multi) + "x", 1, (150,255,150)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.975)) #Position text at bottom of page in center
    textRect.centery = (math.floor(50))
    gameDisplay.blit(text, textRect)

    modeBar = pygame.Surface((display_width*0.28,50)) 
    modeBar.set_alpha(150) #Make bar partly transparent
    modeBar.fill((20,50,150))          
    gameDisplay.blit(modeBar, (display_width*0.66,25)) 

    text = font.render("(E) Mode: " + mode, 1, (150,255,150)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.81)) #Position text at bottom of page in center
    textRect.centery = (math.floor(50))
    gameDisplay.blit(text, textRect)


    if fuel <= 0:

        if timeEnd:

            endTime = pygame.time.get_ticks()//1000

            endMin = endTime // 60

            endSec = endTime - 60*endMin

            timeEnd = False

        timeStr = str(endMin).zfill(2) + ":" + str(endSec).zfill(2)

        player.accX = 0
        player.accY = 0
        player.adv = False
        player.dir = 0

        loseBar = pygame.Surface((display_width*0.4,100)) 
        loseBar.set_alpha(200) #Make bar partly transparent
        loseBar.fill((255,50,20)) #Colour bar blue           
        gameDisplay.blit(loseBar, (display_width*0.3,display_height*0.5))

        font.set_bold(True)
    
        text = font.render("Game Over", 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability

        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+22.5))
        gameDisplay.blit(text, textRect)

        font.set_bold(False)

        text = font.render("Out of fuel", 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability

        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+50))
        gameDisplay.blit(text, textRect)

        text = font.render("Press Esc to quit to menu", 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability

        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+80))
        gameDisplay.blit(text, textRect)

        #Sorting printed to display
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    os.execl(sys.executable, sys.executable, * sys.argv) #Program exits if ESC pressed

                if event.key == pygame.K_e: # Next 8 lines used to toggle between bubbleSort and MergeSort with one button press
                    if alphaOrNumeric == True:
                        bubbleSort(printList)
                        alphaOrNumeric = False # Changes false to true, the 'toggle'
        
                    elif alphaOrNumeric == False:
                        mergeSort(printList)
                        alphaOrNumeric = True

        # Below is a visual representation of the sorted list above, orders based on whats in the list
        # Could have been a FOR loop but works so left for now

        text = font.render("Total Credits: " + str(money), 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.3))
        gameDisplay.blit(text, textRect)

        text = font.render("Final Multiplier: " + str(multi) + "x", 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.35))
        gameDisplay.blit(text, textRect)

        text = font.render("Time Elapsed: " + timeStr, 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.4))
        gameDisplay.blit(text, textRect)
        
        text = font.render("Total Items Collected", 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+140))
        gameDisplay.blit(text, textRect)
        
        text = font.render(printList[0] + ": " + str(totalItems[ str(printList[0]).lower() ]), 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+170))
        gameDisplay.blit(text, textRect)

        text = font.render(printList[1] + ": " + str(totalItems[ str(printList[1]).lower() ]), 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+200))
        gameDisplay.blit(text, textRect)

        text = font.render(printList[2] + ": " + str(totalItems[ str(printList[2]).lower() ]), 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+230))
        gameDisplay.blit(text, textRect)

        text = font.render(printList[3] + ": " + str(totalItems[ str(printList[3]).lower() ]), 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+260))
        gameDisplay.blit(text, textRect)

        text = font.render("Press 'E' to reorder by numerical or alphabetical order", 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+320))
        gameDisplay.blit(text, textRect)

    pygame.display.update()

    #Clock ticks to run at FPS

while not gameExit:

    mineShow = False
    
    if gameOver == True:

        #Finishes the game by printing to the console and ending the loop
        print("GameOver")
        gameExit = True

    #Obtain all user events as a sequence and put them in a for loop
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LCTRL] and pressed[pygame.K_m]: #if CTRL and M pressed...
            menuv2.mainMenu() #...Go back to menu

        if event.type == pygame.KEYDOWN: #When key is down
            if event.key == pygame.K_a: #A button turns ship left
                    player.rotL()
            if event.key == pygame.K_d: #D button turns ship right
                    player.rotR()
            if event.key == pygame.K_w: #W accelerates the ship
                    player.fwd()
            if event.key == pygame.K_s:
                    player.bwd()
            if event.key == pygame.K_m:
                        mine(mineArg[0],mineArg[1],mineArg[2],mineArg[3])
                        mineText = "Press M to mine"
            if event.key == pygame.K_e:
                        mode = "CPU"
                        fuel = 100
            if event.key == pygame.K_ESCAPE:
                    menuv2.pauseMenu()
            if event.key == pygame.K_p: #P for fullscreen lol
                    
                    if fullscreenStat == True:
                         
                            winMode = pygame.DOUBLEBUF | pygame.HWSURFACE
                            display_width = 1200
                            display_height = 800
                            gameDisplay = pygame.display.set_mode((display_width, display_height),winMode)
                            fullscreenStat = False
                    else:
                       
                            winMode = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN #Set display variable to include fullscreen
                            display_width = 1200
                            display_height = 800
                            gameDisplay = pygame.display.set_mode((display_width, display_height),winMode) #Generate new display fullscreen
                            #player.reload()
                            fullscreenStat = True
        
        if event.type == pygame.KEYUP: #When key is released
            if event.key == pygame.K_a or event.key == pygame.K_d: #Stop rotation if A or D was released
                    player.rot = 0
            if event.key == pygame.K_w: #Stop accelerating if W is released
                    player.adv = False
            if event.key == pygame.K_s:
                    player.decc = False
        

        #Allows a user to close the window using the close button
        if event.type == pygame.QUIT:
                gameOver = True
                
    #Undraw objects with black, call all update methods for objects
                
    render()

    clock.tick(FPS)

    if mode == "CPU" and nList != False and len(nList) > 1:

        automate(nList)
    
    #Update display
    

#Close window, end game
pygame.quit()



                
            
    
    
