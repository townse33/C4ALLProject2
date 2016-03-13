import pygame, random, math, menuv2, os, sys
from random import *
from astar import *

#Importing all required libraries and files for the program

pygame.mixer.pre_init(44100,16,2,4096)#Background Music
pygame.init() #Initialise pygame

#Background Music
pygame.mixer.music.load("backgroundsongofchoice.mp3")#As you probably know song should be in the game folder
pygame.mixer.music.set_volume(0)#Volume
pygame.mixer.music.play(-1)#This loops the song

nList = False #Used to store the list of nodes calculated from the A* route globally
npcList = list() #Stores all NPC objects in a list

#Colour palette 
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
pblue = (0,0,255)

npcNo = 20 # Number of NPCs to spawn

mineShow = False #By default, do not show mining notification bar
mineText = "Sell or refuel here!" #Default notification text
#Muted colours for inventory items
invred = (195,60,60)
invyellow = (190,210,110)
invgreen = (105,185,130)
invblue = (135,206,250)
invSize = 0 #Global inventory size
invNote = False #Bool for full inventory notification
shopNote = False #Bool for shop planet notification

mode="Player" #Default control mode is player control

fuel = 100 #Global fuel
texFuel = 100 #Text update variable for fuel

mineArg = [0,0,0,0] #Default mineral quantities at each planet 

#Used for periodic functions
timeR = 0
timeR2 = 0
timeN = 0
timeF = 0
timeF2 = 0

gCredits = 0 #Stores change in credits for notification

#Window dimensions; resolution
display_width = 1200
display_height = 800

winMode = pygame.DOUBLEBUF | pygame.HWSURFACE #Double buffer rendering, hardware acceleration when available

gameDisplay = pygame.display.set_mode((display_width, display_height),winMode) #Initialise pygame window

#Title and caption
pygame.display.set_caption("C4 ALL Project 2: Star Hunt")

#Defines update speed, initialised pygame clock
updateSpeed = 150 
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

idCounter = 0 #Increments over planet instances as a naming convention

multi = 1 #Default credit multiplier

def sellInventory(modList, money,amountL = "",m="",iSize=""):
    global invSize, gCredits, multi
    """ Will output the amount of money gained from selling all the items
    as well as removing all the items sold from the inventory """

    if amountL == "":
        amountL = itemAmount
        m = multi
        iSize = invSize
        gCredits = 0
    
    for i in modList: # Adds money, using the itemCost dictionary
        money += itemCost[ i ] * amountL[ i ] * m
        if amountL == itemAmount:
            gCredits += itemCost[ i ] * itemAmount[ i ] * m
        
    amountL["nebulium"] = 0 #Defaults the dictionary amounts to 0, removing them from the inventory
    amountL["bismuth"] = 0
    amountL["polonium"] = 0
    amountL["francium"] = 0

    iSize = 0
    
    return(money)

    # Found that iterating over the list caused a problem with List Aliasing
    # and removing items from the list being iterated over

def mine(n,b,p,f,amountL = "",iSize ="",tItems=""):

    """Takes 4 int arguments: the frequency of minerals on the planet to
    be mined. Randomly outputs collected mineral quantities, ensuring these
    are not over the inventory size limit of 20"""

    global inventory, invSize, itemAmount, totalItems

    if amountL == "":

        amountL = itemAmount
        iSize = invSize
        tItems = totalItems

    iSize = 0
        
    for mineral in amountL:

        iSize += amountL[mineral] #Find inventory size by iteration
    
    if iSize < 20:

            neb = randint(0,n) #Randomly define output mineral quanities
            bis = randint(0,b)
            pol = randint(0,p)
            fra = randint(0,f)

            amountL["nebulium"] += neb #Add these to the appropiate lists
            amountL["bismuth"] += bis
            amountL["polonium"] += pol
            amountL["francium"] += fra

            tItems["nebulium"] += neb
            tItems["bismuth"] += bis
            tItems["polonium"] += pol
            tItems["francium"] += fra

            iSize = 0

            for mineral in amountL: #Check inventory size again

                iSize += amountL[mineral]

            while iSize > 20: #If size limit exceeded, randomly remove gained mineral

                ranMat = choice(inventory)

                if amountL[ranMat] > 0:

                    amountL[ranMat] -= 1

                iSize = 0

                for mineral in amountL:

                    iSize += amountL[mineral]

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


#Class System
class Ship:
        """This class deals with player controlled movement"""

        def __init__(self, display_width, display_height):

            Ship = pygame.image.load("spaceship.png") #Load the sprite image
            
            self.dir = 0 #Direction of ship in degrees, taken from a north bearing
            self.rot = 0 #Current rotation amount
            self.posX = 0 #X position of player on map
            self.posY = 0 #Y position of player on map
            self.velX = 0 #X acceleration of player
            self.velY = 0 #Y acceleration of player
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
                
                self.velX -= math.sin(math.radians(self.dir))*0.02 #Sine rule to find change in player X velocity
                self.velY -= math.sin(math.radians(90-self.dir))*0.02 #Sine rule to find change in player Y velocity

                fuel -= 0.15 #Decrease fuel when accelerating

            if self.decc == True: #For gradual decceleration, decrease velocity values fractionally

                self.velX *= 0.99
                self.velY *= 0.99

            #Rotate ship to current direction
            Ship = pygame.transform.rotate(pygame.image.load("spaceship.png"),self.dir)

            spriteW, spriteH = Ship.get_size() #Obtain sprite dimensions

            gameDisplay.blit(Ship, (display_width/2-spriteW*0.5,display_height/2-spriteH*0.5)) #Initially blit considering the sprite dimensions

            self.posX +=self.velX #Update X position, note that Y axis is inverted
            self.posY -=self.velY

        def rotL(self):
            self.rot = 1 #Rotate anticlockwise 1 degree per frame
        def rotR(self):
            self.rot = -1 #Rotate clockwise 1 degree per frame
            
        def fwd(self):
            self.adv = True #Begin accelerating

        def bwd(self):
            self.decc = True #Begin deccelerating

            
class SpaceObject:
    """Class for all objects that need scrolling"""

    def __init__(self, posX, posY, img, N=0,B=0,P=0,F=0,shop=False): #In addition to position, an image is required, mining parameters are 0 by default, planets are not shops by default

        global universe, inMemory, idCounter

        Object = pygame.image.load("planets/" + img) #This time, we take an image as a string as a parameter too

        self.sW, self.sH = Object.get_size()

        self.posX = posX
        self.posY = posY
        self.disX = posX + self.sW/2  #Centering only affects an object's initial screen position so this is done before the blit, multipliers to compensate for pygame's bad centering
        self.disY = posY + self.sH /2

        
        self.img = "planets/" + img #We maintain the image path as an attribute so it need only be provided once
        self.n = N #Mining parameters
        self.b = B
        self.p = P
        self.f = F
        self.inMem = False #Planet does not start in memory
        self.id = idCounter #Assign global ID to planet

        idCounter +=1 #Increment ID for next planet

        self.shop = shop #Shop attribute

        gameDisplay.blit(Object, (self.disX,self.disY))

        universe.append(self)
    
    def update(self,toBlit):

        global mineShow,display_width,display_height,money,fuel,mineArg,shopNote,invNote,invSize

        if not(toBlit):

            self.disX -= player.velX #Evaluate difference in object to player position on the screen
            self.disY -= player.velY

        if toBlit:
            
            Object = pygame.image.load(self.img)

            pygame.Surface.convert(Object) #Images are converted by pygame for optimal speed

            gameDisplay.blit(Object, (math.floor(self.disX+self.sW*0.39),math.floor(self.disY-self.sH*0.04))) #We use floor division as we cannot have fractional pixels, constants added to reduce image offset issues

            if abs(self.disX+self.sW/2-display_width/2) < 250 and abs(self.disY+self.sH/3-display_height/2) < 250: #If within range of planet (adjusted for offset)

                mineShow = True 
                fuel = 100

                if self.shop:

                    mineArg = [0,0,0,0]

                    if invSize>0: #Inventory will automatically be sold at a shop planet
                        money = sellInventory(inventory,money)
                        invNote = True
                        

                    shopNote = True

                else:

                    mineArg = [self.n,self.b,self.p,self.f]
                    shopNote = False
                    invNote = False
npcCounter = 0
class npc():

    def __init__(self,posX,posY,img="spaceship.png"):

        global npcList, npcCounter

        self.posX = posX
        self.posY = posY
        self.dir = randint(0,360)
        self.velX = 0
        self.velY = 0

        self.img = img

        self.money = 0
        self.fuel = 100
        self.multi = 1
        self.itemAmount = {"nebulium":0, "bismuth":0, "polonium":0, "francium":0}
        self.invSize = 0
        self.totalItems = {"nebulium":0, "bismuth":0, "polonium":0, "francium":0}

        self.name = "NPC" + str(npcCounter)

        npcCounter +=1

        self.nList = False

        npcList.append(self)

    def update(self):

        global nodeList, universe, inventory

        while self.nList == False:

            ranNode = randint(0,len(nodeList)-1)

            self.nList = pathFind(ranNode)

        if len(self.nList)> 1:

            self.currNode = universe[int(self.nList[-2][1:])] #Finds the equivalent planet to the node given to the automation function

            targetDir = math.degrees(math.atan2(self.currNode.posY+self.posY,self.currNode.posX-self.posX))-90

            if targetDir < 0:

                targetDir +=360

            if abs(self.dir-targetDir)>1:

                self.velX = 0
                self.velY = 0

                self.dir += 1

                if self.dir > 360:

                    self.dir = self.dir % 360

                npcObject = pygame.transform.rotate(pygame.image.load(self.img),self.dir)

                self.sW, self.sH = npcObject.get_size() 

                gameDisplay.blit(npcObject, (self.posX-player.posX-self.sW*0.5,self.posY-self.sH*0.5+player.posY))

                return
            
            self.dir = targetDir

            dis = ((self.posX-self.currNode.posX)**2+(self.currNode.posY-self.posY)**2)**0.5 #Pythagoras to find distance to object


            if dis < 500: #Consider a distance of 5 to the object as an acceptable range to stop

                    self.velX = 0
                    self.velY = 0
                    self.fuel = 100

                    self.nList.pop(-2) #Remove visited nodes

                    mine(self.currNode.n,self.currNode.b,self.currNode.p,self.currNode.f,self.itemAmount,self.invSize,self.totalItems) #Mine automatically at the visited planet

                    if len(self.nList) == 1:
                
                        self.money = sellInventory(inventory,self.money,self.itemAmount,self.multi,self.invSize) #Automatically sell inventory if goal reached

                        print(str(self.name) + " has earned " + str(self.money) + " credits!")

                        self.nList = False
            else:

                self.velX -= math.sin(math.radians(self.dir))*0.04 
                self.velY -= math.sin(math.radians(90-self.dir))*0.04 

                self.posX +=self.velX 
                self.posY +=self.velY

                npcObject = pygame.transform.rotate(pygame.image.load(self.img),self.dir)
                self.sW, self.sH = npcObject.get_size() 
                gameDisplay.blit(npcObject, (self.posX-player.posX-self.sW*0.5,self.posY+player.posY-self.sH*0.5))

                self.fuel -=0.15

                return
            

def ranValue(): #Randomise mineral values
    global inventory, itemCost
    for item in inventory:
        itemCost[item] = randint(10,100)
    
#Game states
gameExit = False
gameOver = False

#init player
player = Ship(display_width/2, display_height/2)

fullscreenStat = False

def secGen(startW,endW,startH,endH,planetNo,spread):

    """Generates one section of the universe, as defined by the parameters.
    PlanetNo can be used to control average planets per section, spread can forcibly
    increase their distance from each other"""
    
    global planetID

    testList = list()

    for k in range(planetNo): #Select random coordinates
    
        ranX = randint(startW,endW)
        ranY = randint(startH,endH)

        for planet in testList:

            loop = True

            while loop: #Test that the planet to be generated is not too close to any others in the section or the edge

                test1 = planet.posX > ranX - spread
                test2 = planet.posX < ranX + spread

                test3 = planet.posY > ranY - spread
                test4 = planet.posY < ranY + spread

                test5 = ranX > startW + spread
                test6 = ranX < endW - spread

                test7 = ranY > startH + spread
                test8 = ranY < endW - spread
                
                if (test1 and test2) and (test3 and test4): #Randomise again if tests failed

                    ranX = randint(startW,endW)
                    ranY = randint(startH,endH)

                else:

                    loop = False
                    
        ranImg = choice(os.listdir("Planets/")) #Select random planet image from image directory

        print(ranImg)

        r1 = randint(0,4) #Randomise mineral frequencies
        r2 = randint(0,4)
        r3 = randint(0,4)
        r4 = randint(0,4)

        if ranImg == "earth.jpg": #Earthlike planets are shops

            shopRan = True

        else:

            shopRan = False

        planetID = SpaceObject(ranX,ranY,ranImg,r1,r2,r3,r4,shopRan) #Initialise generated planet

        testList.append(planetID) #Add planet to list of planets to test for proximity

uniGraph = dict() #Dictionary to represent all universe objects as a mathematical graph
fuelDis = 2000 #Any planet further away than the predetermined max distance for fuel is considered disconnected
    
                
def universeGen(uniH,uniW,secPlanets,spread):

    """Generates universe, section by section. Takes dimensions of universe and automatically centers it.
    secPlanets is used for average planets per section, spread defines the factor for minimum proximity"""

    global universe, uniGraph, fuelDis, nodeList, display_height, display_width
                
    universeH = uniH
    universeW = uniW

    secNo = (universeH * universeW) / (display_height * display_width) #A section is defined as one screen area

    rowX = -universeW/2 #Start at bottom left corner of universe
    colY = -universeH/2

    nodeList = list()

    for column in range(universeH//display_height): #Generate each section of planets, by row, then column
        for row in range(universeW//display_width):
            secGen(row*display_width+rowX,(row+1)*display_width+rowX,column*display_height+colY,(column+1)*display_height+colY,secPlanets,spread)
    nodeID = 0
    for planet in universe: #Convert each planet object to node for later use

        planetNode = "n" + str(planet.id)

        planetNode = addNode(planetNode,planet.posX,planet.posY,"n" + str(planet.id))

        nodeList.append(planetNode)

    for node in nodeList:
    #If the modulus of the distance between planets is less than the max fuel distance, then it is considered adjacent

        adjList = list()

        for planet2 in nodeList:

            test = ((planet2.x - node.x)**2+(planet2.y-node.y)**2)**0.5 < fuelDis

            if test:

                adjList.append(planet2)
                
        uniGraph[node] = adjList
        #Graph is stored as a dictionary with nodes as keys and adjacent nodes as values



def pathFind(target):

    """Prepares a graph and target to pass to the A* algorithm"""

    global universe, player, uniGraph, fuelDis, nodeList

    addList = list()

    for planet in universe:

        #Find nodes adjacent to the player

        if abs(planet.disX) < fuelDis and abs(planet.disY) < fuelDis:

            addList.append(nodeList[planet.id])
            
    start = addNode("start",player.posX+1,player.posY+1,"start")

    nodeList.append(start)

    uniGraph[start] = addList

    return aStar(uniGraph,start,nodeList[target]) #Perform the A* algorithm on the given target

def automate(nodeL):

    global nodeList, fuel, player, universe, display_height,display_width, prevNode, inventory, money, clock, updateSpeed, mode

    print(nodeL)

    player.velX = 0
    player.velY = 0
    player.adv = False
    player.decc = False

    #Cease movement to ensure automation works as expected

    while len(nodeL)> 1:

        currNode = universe[int(nodeL[-2][1:])] #Finds the equivalent planet to the node given to the automation function

        print(currNode.id,currNode.posX,-currNode.posY) #Prints headed coordinates

        targetDir = math.degrees(math.atan2(-currNode.posY-player.posY,currNode.posX-player.posX))-90
        #The concept of polar co-ordinates is used to find target bearing, using the arctan2 function to find the angle
        #as though it was a complex argument, converted to degrees

        if targetDir < 0:

            targetDir = targetDir + 360

        while int(player.dir) != int(targetDir):

            player.rot = -1

            render() #Ensure rendering and user input functions are working whilst automation begins
            cpuEvents()
            if mode == "Player": #Abort automation if mode changed

                return
            clock.tick(updateSpeed)
        
        player.dir = targetDir

        print(player.dir)
        print(targetDir)

        render()

        player.rot=0

        loop = True

        player.adv = True

        while loop:

            dis = ((player.posX-currNode.posX)**2+(player.posY+currNode.posY)**2)**0.5 #Pythagoras to find distance to object

            targetDir = math.degrees(math.atan2(-currNode.posY-player.posY,currNode.posX-player.posX))-90 #Bearing recalculated
            if abs(targetDir-player.dir) > 0:

                player.dir = targetDir #If off course, immediately adjust

            if dis < 5: #Consider a distance of 5 to the object as an acceptable range to stop

                player.adv = False

                player.velX = 0
                player.velY = 0

                loop = False

                fuel = 100

            render()

            cpuEvents()

            if mode == "Player":

                return

            clock.tick(updateSpeed)

        nodeL.pop(-2) #Remove visited nodes

        mine(currNode.n,currNode.b,currNode.p,currNode.f) #Mine automatically at the visited planet

        prevNode = currNode.id #Used to ensure the planet is not discarded from memory upon visiting it

        if len(nodeL) == 1:

            money = sellInventory(inventory,money) #Automatically sell inventory if goal reached

            return True

        player.decc = False

universeGen(10000,10000,1,200) #Generates universe

prevNode = 0

def cpuEvents():
    global mode, display_width, display_height, winMode, gameDisplay, fullscreenStat

    for event in pygame.event.get(): 

            if event.type == pygame.KEYDOWN:
        
                if event.key == pygame.K_e: #E to change mode
                            mode = "Player"
                if event.key == pygame.K_ESCAPE: #Escape pauses game
                        menuv2.pauseMenu()
                if event.key == pygame.K_p: #P for fullscreen lol
                        
                        if fullscreenStat == True: #Toggle fullscreen off
                             
                                winMode = pygame.DOUBLEBUF | pygame.HWSURFACE
                                display_width = 1200
                                display_height = 800
                                gameDisplay = pygame.display.set_mode((display_width, display_height),winMode)
                                fullscreenStat = False
                        else: #Toggle fullscreen on
                           
                                winMode = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN #Set display variable to include fullscreen
                                display_width = 1200
                                display_height = 800
                                gameDisplay = pygame.display.set_mode((display_width, display_height),winMode) #Generate new display fullscreen
                                #player.reload()
                                fullscreenStat = True
        
        #Allows a user to close the window using the close button
            if event.type == pygame.QUIT:
                os.execl(sys.executable, sys.executable, * sys.argv)
                
timeEnd = True #used to prevent game timer continuing after gameover

for nID in range(npcNo):

    npcID = "npc" + str(nID)

    npcID = npc(randint(-5000,5000),randint(-5000,5000))

def render():

    global npc1,npcList,npcNo,endTime,endMin,endSec,timeStr,timeEnd,mode, prevNode, multi, ranNode, nodeList, nList, winMode, white, red, green, pblue, totalItems, money, black, shopNote, invred, invyellow, invgreen, invblue, gameDisplay, inMemory, memLimit, universe, fuel, display_width, display_height, inventory, texX, texY, texFuel, texSpeed, timeR, timeR2, timeF, timeF2, itemAmount, mineText, mineShow, invSize, invNote, gCredits, printList, alphaOrNumeric, clock, updateSpeed
    #Many variables are declared as global as it would not be feasible to pass all of these between the necessary functions
    #Fill unused space with black
    gameDisplay.fill(black)

    while nList == False:
        #A random planet is selected to hold a multiplier, A* is used to find if it is possible to visit it

        #If impossible, new nodes will be tried until a path is possible

        ranNode = randint(0,len(nodeList)-1)

        nList = pathFind(ranNode)
     
    if len(nList)>1:

        #Obtain multiplier coordinates

        mulX = universe[int(nList[0][1:])].posX
        mulY = -universe[int(nList[0][1:])].posY

        if universe[int(nList[-2][1:])].inMem == False:

            #Ensure multiplier planet is in memory as a priority

            universe[int(nList[-2][1:])].inMem=True
            inMemory.append(universe[int(nList[-2][1:])])
            
    else:

        #Increase multiplier if the automated player finishes the A* path

        multi += 1
        nList = False
        mulX = "N/A"
        mulY = ""
        

    if universe[prevNode].inMem == False: #Ensure previous node in path does not abruptly disappear

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

    for npc in npcList:

        npc.update()
            
    player.update() #Update player object

    font = pygame.font.Font("trench.otf", 36) #Defines sci-fi font from external file

    #Intentionally slow down text updates, it is very distracting and hard to read when they are updated once per frame
    if pygame.time.get_ticks() % 4 == 0:
            texY = player.posY
            texX = player.posX
            texSpeed = round(40*math.sqrt((player.velX)**2+(player.velY)**2),1) #Speed is defined as 40 times the modulus of the velocities in km/s
            if fuel < 0: #Prevents negative fuel quantities
                texFuel = 0
            else:
                texFuel = round(fuel,2)
                
    #stat bar
    statBar = pygame.Surface((display_width,36)) #Create a stats GUI bar as a surface
    statBar.set_alpha(200) #Make bar partly transparent                
    statBar.fill((20,50,150)) #Colour bar blue           
    gameDisplay.blit(statBar, (0,display_height-36)) #Render GUI bar at bottom of screen   

    text = font.render("X: " + str(math.floor(texX)) + "        Y: " + str(math.floor(texY)) + "        Speed: " + str(texSpeed) + "km/s" + "        Credits: " + str(money) + "        Fuel:" + str(texFuel) + "%", 1, (100, 200, 255)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
    textRect.centery = (math.floor(display_height-18))
    gameDisplay.blit(text, textRect)

    #inventory bar
    inventoryBar = pygame.Surface((display_width*0.3,90)) 
    inventoryBar.set_alpha(150) 
    inventoryBar.fill((20,50,150))           
    gameDisplay.blit(inventoryBar, (display_width*0.35,5))

    
    #Every minute, randomise mineral values
    if timeR < 60000:
        timeR = pygame.time.get_ticks() - timeR2
    else:
        timeR2 = pygame.time.get_ticks()
        timeR = 0
        ranValue()

    #Every 2 seconds, deplete fuel by 1%
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

    if mode == "Player": #In player mode show the appropiate player mode notification

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
    else: #If CPU control, display pathfinding message instead

        noteColour = (200, 160, 80)

        fillColour = (20,50,150)

        showBar = True

        mineText = "Pathfinding..."

    if showBar:

        #Notification bar
        mineBar = pygame.Surface((display_width*0.3,45)) 
        mineBar.set_alpha(150) 
        mineBar.fill(fillColour)          
        gameDisplay.blit(mineBar, (display_width*0.35,100)) 

        text = font.render(mineText, 1, noteColour) 
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5))
        textRect.centery = (math.floor(125))
        gameDisplay.blit(text, textRect)

    #Multiplier coordinate bar
    mulBar = pygame.Surface((display_width*0.34,50)) 
    mulBar.set_alpha(150) #Make bar partly transparent
    mulBar.fill((20,50,150))          
    gameDisplay.blit(mulBar, (0,25)) 

    text = font.render("Multiplier at: " + str(mulX) + "," + str(mulY), 1, (100, 200, 255)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.17)) #Position text at bottom of page in center
    textRect.centery = (math.floor(50))
    gameDisplay.blit(text, textRect)

    #Multiplier bar
    mul2Bar = pygame.Surface((display_width*0.05,50)) 
    mul2Bar.set_alpha(150) #Make bar partly transparent
    mul2Bar.fill((20,50,150))          
    gameDisplay.blit(mul2Bar, (display_width*0.95,25)) 

    text = font.render(str(multi) + "x", 1, (150,255,150)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.975)) #Position text at bottom of page in center
    textRect.centery = (math.floor(50))
    gameDisplay.blit(text, textRect)

    #Control mode bar
    modeBar = pygame.Surface((display_width*0.28,50)) 
    modeBar.set_alpha(150) #Make bar partly transparent
    modeBar.fill((20,50,150))          
    gameDisplay.blit(modeBar, (display_width*0.66,25)) 

    text = font.render("(E) Mode: " + mode, 1, (150,255,150)) #Render GUI text, floor division used for variables for readability
    textRect = text.get_rect()
    textRect.centerx = (math.floor(display_width*0.81)) #Position text at bottom of page in center
    textRect.centery = (math.floor(50))
    gameDisplay.blit(text, textRect)


    if fuel <= 0: #When GameOver

        if timeEnd: #Calculate elapsed game time, store in MM:SS format

            endTime = pygame.time.get_ticks()//1000

            endMin = endTime // 60

            endSec = endTime - 60*endMin

            timeEnd = False

        timeStr = str(endMin).zfill(2) + ":" + str(endSec).zfill(2)

        player.velX = 0 #Prevent player from moving
        player.velY = 0
        player.adv = False
        player.dir = 0

        #GameOver bar
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

        text = font.render("(Q) Print Leaderboard (ESC) Quit", 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability

        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+80))
        gameDisplay.blit(text, textRect)

        #Sorting printed to display
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    os.execl(sys.executable,sys.executable)
                     #Program exits if ESC pressed

                if event.key == pygame.K_e: # Next 8 lines used to toggle between bubbleSort and MergeSort with one button press
                    if alphaOrNumeric == True:
                        bubbleSort(printList)
                        alphaOrNumeric = False # Changes false to true, the 'toggle'
        
                    elif alphaOrNumeric == False:
                        mergeSort(printList)
                        alphaOrNumeric = True
                        
                if event.key == pygame.K_q:
                    gameDisplay.fill(black)
                    unsortD = dict()
                    for npc in npcList:
                        unsortD[npc.money] = npc
                    sortL = list(unsortD.keys())
                    mergeSort(sortL)
                    for money in sortL:
                        print(str(unsortD[money].name) + ": " + str(money) +  " credits")

        #GameOver Stats

        text = font.render("Total Credits: " + str(money), 1, (255, 255, 255)) 
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) 
        textRect.centery = (math.floor(display_height*0.3))
        gameDisplay.blit(text, textRect)

        text = font.render("Final Multiplier: " + str(multi) + "x", 1, (255, 255, 255)) 
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) 
        textRect.centery = (math.floor(display_height*0.35))
        gameDisplay.blit(text, textRect)

        text = font.render("Time Elapsed: " + timeStr, 1, (255, 255, 255)) 
        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) 
        textRect.centery = (math.floor(display_height*0.4))
        gameDisplay.blit(text, textRect)

        #Final inventory list for sorting
        
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

    #Clock ticks to run at updateSpeed

while True:

    mineShow = False

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
            if event.key == pygame.K_s: #S deccelerates ship
                    player.bwd()
            if event.key == pygame.K_m: #M mines a planet if nearby
                        mine(mineArg[0],mineArg[1],mineArg[2],mineArg[3])
                        mineText = "Press M to mine"
            if event.key == pygame.K_e and fuel > 0: #Switches to CPU control mode (but prevents this on GameOver)
                        mode = "CPU"
                        fuel = 100
            if event.key == pygame.K_ESCAPE: #Escape to pause
                    menuv2.pauseMenu()
            if event.key == pygame.K_p: #P for fullscreen
                    
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
            if event.key == pygame.K_s: #Stop deccelerating is S released
                    player.decc = False
        

        #Allows a user to close the window using the close button
        if event.type == pygame.QUIT:
            os.execl(sys.executable, sys.executable, * sys.argv)
                    
                
    render() 

    clock.tick(updateSpeed) #Updates clock at update speed

    if mode == "CPU" and nList != False and len(nList) > 1: #If CPU mode and path exists, run automation function 

        automate(nList)
    

#Close window, end game
pygame.quit()



                
            
    
    
