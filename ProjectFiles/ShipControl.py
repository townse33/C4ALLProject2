import pygame
import time
import random
import math

pygame.init()

#Colour palette 
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,255)

#Window dimensions; resolution
display_width = 1200
display_height = 800

gameDisplay = pygame.display.set_mode((display_width, display_height)) #Initialise pygame window

#Title and caption
pygame.display.set_caption("C4 ALL Project 2")

#Time Variables, initialise FPS clock
FPS = 60
clock = pygame.time.Clock()

#Universe object list (for later use)
universe = []

class Ship:
        """This class deals with player controlled movement"""

        def __init__(self, display_width, display_height):

            Ship = pygame.image.load("spaceship.png") #Load the sprite image
            
            self.dir = 0 #Direction of ship in degrees, taken from a north bearing
            self.rot = 0 #Current rotation amount
            self.posX = 0 #X position of player on map
            self.posY = 0 #Y position of player on map
            self.dW = display_width #Screen width
            self.dH = display_height #Screen height

            self.adv = False #Is ship accelerating?
            

            #store ship image dimensions
            self.sW, self.sH = Ship.get_size()

            #centre ship by subtracting half ship size from given dimensions
            gameDisplay.blit(Ship, (self.dW-self.sW*0.5,self.dH-self.sH*0.5))

        def update(self):


            #Modulo on direction to prevent direction exeeding 360 degrees
            self.dir = self.dir % 360
            #Increment direction by rotation amount
            self.dir += self.rot
            
            if self.adv == True:
                
                self.posX += -math.sin(math.radians(self.dir))*0.025 #Sine rule to find change in player X position
                self.posY += -math.sin(math.radians(90-self.dir))*0.025 #Sine rule to find change in player Y position

            #Rotate ship to current direction
            Ship = pygame.transform.rotate(pygame.image.load("spaceship.png"),self.dir)

            spriteW, spriteH = Ship.get_size()

            gameDisplay.blit(Ship, (self.dW-spriteW*0.5,self.dH-spriteH*0.5))

        def rotL(self):
            self.rot = 2 #Rotate anticlockwise 2 degrees per frame
        def rotR(self):
            self.rot = -2 #Rotate clockwise 2 degrees per frame
            
        def fwd(self):
            self.adv = True 
            
        

class NotAShip:
    """Placeholder class used for objects that are not the player, i.e. ones that need scrolling"""

    def __init__(self, posX, posY, img):

        Object = pygame.image.load(img) #This time, we take an image as a string as a parameter too


        self.sW, self.sH = Object.get_size()

        self.posX = posX
        self.posY = posY
        self.scrX = posX-self.sW*0.5 #Centering only affects an object's initial screen position so this is done before the blit
        self.scrY = posY-self.sH*0.5
        self.img = img #We maintain the image path as an attribute so it need only be provided once


        gameDisplay.blit(Object, (self.scrX,self.scrY))

    
    def update(self):

        self.scrX += -player.posX #Evaluate difference in object to player position on the screen
        self.scrY += -player.posY

        Object = pygame.image.load(self.img)

        gameDisplay.blit(Object, (math.floor(self.scrX),math.floor(self.scrY))) #We use floor division as we cannot have fractional pixels


#Game states
gameExit = False
gameOver = False

#Screen position variables: DO NOT CONFUSE WITH PLAYER POSITION
scrPos_x = display_width/2
scrPos_y = display_height/2

#init player
player = Ship(scrPos_x, scrPos_y)

other = NotAShip(500,300,"earth.png")

while not gameExit:
    
    if gameOver == True:

        #Finishes the game by printing to the console and ending the loop
        print("GameOver")
        gameExit = True
        

    #Obtain all user events as a sequence and put them in a for loop
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN: #When key is down
            
            if event.key == pygame.K_a: #A button turns ship left
                    player.rotL()
            if event.key == pygame.K_d: #D button turns ship right
                    player.rotR()
            if event.key == pygame.K_w: #W accelerates the ship
                    player.fwd()
        if event.type == pygame.KEYUP: #When key is released
            if event.key == pygame.K_a or event.key == pygame.K_d: #Stop rotation if A or D was released
                    player.rot = 0
            if event.key == pygame.K_w: #Stop accelerating if W is released
                    player.adv = False
        

        #Allows a user to close the window using the close button
        if event.type == pygame.QUIT:
                gameOver = True
    
    #Undraw objects with black, call all update methods for objects
    gameDisplay.fill(black)

    other.update()

    player.update()

    pygame.display.update()

    #Clock ticks to run at FPS
    clock.tick(FPS)



#Close window, end game
pygame.quit()



                
            
    
    
