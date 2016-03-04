import pygame
import time
import random

pygame.init()

#colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,255)

display_width = 1200
display_height = 800

gameDisplay = pygame.display.set_mode((display_width, display_height))

#Title
pygame.display.set_caption("Whatever its called")

#Time Variables
FPS = 30
clock = pygame.time.Clock()

class spaceShip:

    def __init__(self, display_width, display_height):

        spaceShip = pygame.image.load("spaceship.png")

        #store ship image dimensions
        shipW, shipH = spaceShip.get_size()

        #centre ship by subtracting half ship size from given dimensions
        gameDisplay.blit(spaceShip, (display_width-shipW*0.5,display_height-shipH*0.5))
    

#Game states
gameExit = False
gameOver = False

#Position variables
lead_x = display_width/2
lead_y = display_height/2


while not gameExit:
    
    if gameOver == True:
        
        print("GameOver")
        gameExit = True
        

    for event in pygame.event.get():
        if event.type == pygame.K_q:
                gameOver = True

        #Allows a user to close the window using the close button
        if event.type == pygame.QUIT:
                gameOver = True
    

    gameDisplay.fill(black)

    #Create player object, currently giving half window dimensions as arguments
    player = spaceShip(lead_x, lead_y)

    pygame.display.update()

    #Clock ticks to run at FPS
    clock.tick(FPS)

#Close window, end game
pygame.quit()



                
            
    
    
