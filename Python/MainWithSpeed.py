import pygame, time, math, menuv2, os, sys
from random import *


pygame.mixer.pre_init(44100,16,2,4096)#Background Music
pygame.init()

#Background Music
pygame.mixer.music.load("backgroundsongofchoice.mp3")#As you probably know song should be in the game folder
pygame.mixer.music.set_volume(1)#Volume

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

fuel = 100
texFuel = 100

mineArg = [0,0,0,0]

timeR = 0
timeN = 0

gCredits = 0


#Window dimensions; resolution
display_width = 1200
display_height = 800

winMode = pygame.DOUBLEBUF | pygame.HWSURFACE #| pygame.FULLSCREEN #Enable hardware acceleration, remove first comment for fullscreen


gameDisplay = pygame.display.set_mode((display_width, display_height),winMode) #Initialise pygame window

#Title and caption
pygame.display.set_caption("C4 ALL Project 2")

#Time Variables, initialise FPS clock
FPS = 100 #One frame = Ten milliseconds
clock = pygame.time.Clock()

#Universe stores all object information, inMemory determines what to load
universe = []
inMemory = []
memLimit = 50 #How many objects to leave in memory

texX = 0 #Player X position variable for text, for controlled updating
texY = 0 #Player Y position for text
texSpeed = 0 #Player speed for text

#Inventory setup
itemCost = {"nebulium":39, "bismuth":81, "polonium":56, "francium":93} # Costs of all the items that can be collected
# nebulium == yellow, bismuth == red, polonium == green, francium == blue

inventory = ["nebulium", "bismuth", "polonium", "francium"] # Inventory items collected by the user
itemAmount = {"nebulium":0, "bismuth":0, "polonium":0, "francium":0} #How much of each item the user has
money = 0 # Credits owned by the user


def addToInventory(modList, item):
    modList.append(item)

def sellInventory(modList, money):
    global invSize, gCredits
    """ Will output the amount of money gained from selling all the items
    as well as removing all the items sold from the inventory """

    gCredits = 0
    
    for i in modList: # Adds money, using the itemCost dictionary
        money += itemCost[ i ] * itemAmount[ i ]
        gCredits += itemCost[ i ] * itemAmount[ i ]
        
    itemAmount["nebulium"] = 0
    itemAmount["bismuth"] = 0
    itemAmount["polonium"] = 0
    itemAmount["francium"] = 0

    invSize = 0
    
    # Found that iterating over the list caused a problem with List Aliasing
    # and removing items from the list being iterated over
    
    return(money)

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
                
                self.accX -= math.sin(math.radians(self.dir))*0.005 #Sine rule to find change in player X acceleration
                self.accY -= math.sin(math.radians(90-self.dir))*0.005 #Sine rule to find change in player Y acceleration

                fuel -= 0.1

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

        global universe, inMemory

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
        self.inMem = True #Planet starts in memory

        self.shop = shop

        gameDisplay.blit(Object, (self.disX,self.disY))

        universe.append(self)
        inMemory.append(self)

    
    def update(self):

        global mineShow,display_width,display_height,money,fuel,mineArg,shopNote,invNote,invSize

        self.disX -= player.accX #Evaluate difference in object to player position on the screen
        self.disY -= player.accY

        Object = pygame.image.load(self.img)

        gameDisplay.blit(Object, (math.floor(self.disX),math.floor(self.disY))) #We use floor division as we cannot have fractional pixels

        if abs(self.disX+self.sW/2-display_width/2) < 150 and abs(self.disY+self.sH/2-display_height/2) < 150:

            mineShow = True

            if self.shop:

                mineArg = [0,0,0,0]

                if invSize>0:
                    money = sellInventory(inventory,money)
                    invNote = True
                    

                fuel = 100
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

Object1 = NotAShip(0, 0,"earth.jpg",0,0,0,0,True) #Places aobject
Object2 = NotAShip(600,600,"moon.jpg",1) #Places a Moon object
Object3 = NotAShip(-500,-500,"mars.jpg",3,2,1,1) #Places a Mars object

fullscreenStat = False



 
while not gameExit:
    
    if gameOver == True:

        #Finishes the game by printing to the console and ending the loop
        print("GameOver")
        gameExit = True
        

    #Obtain all user events as a sequence and put them in a for loop
    for event in pygame.event.get():
        pressed = pygame.key.get_pressed()
            

     
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
    gameDisplay.fill(black)

    if len(inMemory) > memLimit: #Check if memory limit exceeded, removed earliest entry in memory list if so
                inMemory[0].inMem = False
                inMemory[0].remove()

    for planet in inMemory: #Update all objects in memory
            planet.update()

    for planet in universe: #Display any unloaded planet if within distance criteria and is not already in memory
            if planet.disX < display_width*1.5 and planet.disX < display_width*-1.5 and planet.disY > display_height*1.5 and planet.disY < display_height*-1.5 and planet.inMem == False:
                    planet.inMem = True
                    inMemory += planet

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


    mergeSort(inventory)

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
        timeR = pygame.time.get_ticks()
    else:
        timeR = 0
        ranValue()
    
    

    """
    inventoryItem1 = pygame.Surface((80,80))
    inventoryItem1.set_alpha(100)
    pygame.draw.rect(inventoryItem1, red, (25, 25, 50, 50), 0)
    pygame.transform.rotate(inventoryItem1,45)
    gameDisplay.blit(inventoryItem1, ((int(display_width*0.5-90), 40) ))
    """

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

            mineText = "Sell or refuel here!"
    elif fuel<25:

        mineText = "Warning: Low Fuel!"

        fillColour = (255,50,20)

        noteColour = (200, 160, 80)

        showBar = True

    else:

        showBar = False

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

    if fuel <= 0:

        player.accX = 0
        player.accY = 0
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

        text = font.render("Press any key to quit to menu", 1, (255, 255, 255)) #Render GUI text, floor division used for variables for readability

        textRect = text.get_rect()
        textRect.centerx = (math.floor(display_width*0.5)) #Position text at bottom of page in center
        textRect.centery = (math.floor(display_height*0.5+80))
        gameDisplay.blit(text, textRect)

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                
                 os.execl(sys.executable, sys.executable, * sys.argv)

    mineShow = False
    
    #Update display
    pygame.display.update()

    #Clock ticks to run at FPS
    clock.tick(FPS)



#Close window, end game
pygame.quit()



                
            
    
    
