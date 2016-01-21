import pygame
import time
import random

#Required to run
pygame.init()

#define colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

#Game Canvas
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))

#Game Title
pygame.display.set_caption("SNAKEY GAME")

#Time Variable
FPS = 20
clock = pygame.time.Clock()

#Screen Text
font = pygame.font.SysFont(None, 25)
score_font = pygame.font.SysFont(None, 65)


"""Snake list draws the snake when eating apple"""
def snake(block_size, snakeList):
    for XnY in snakeList:        
        pygame.draw.rect(gameDisplay, black, [XnY[0],XnY[1],block_size,block_size])

def message_to_screen(msg, colour):
    screen_text = font.render(msg, True, colour)
    gameDisplay.blit(screen_text, [display_width/2, display_height/2])

def score_message(msg, colour):
    screen_text = score_font.render(msg, True, colour)
    gameDisplay.blit(screen_text, [display_width-display_width, display_height-100])


#GameLoop Function
def gameLoop():

    #Constant Variable
    gameExit = False
    gameOver = False
    block_size = 10

    #Position variables
    lead_x = display_width/2
    lead_y = display_height/2

    #Snake Variables
    snakeList = []
    snakeLength = 1

    #Moving Variables
    lead_x_change = 0
    lead_y_change = 0
    movement_speed = 10

    #Apple Generator
    randAppleX = random.randrange(0,int(display_width-(block_size)),block_size)
    randAppleY = random.randrange(0,int(display_height-(block_size)), block_size)

    #Score Variable
    global score
    score = 0
    
    #Game Loop - While gameExit = False
    while not gameExit:
        #Do this when user dies
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game Over, press C to Play again or Q to quit", (0,0,0))
            score_message("Your Final Score was: " + str(score),(0,0,0))
            pygame.display.update()

            #Gets users input and follows the correct actions
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        #Captures all of the events = Button press/Mouse Move
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:

                #Moving Left
                if event.key == pygame.K_LEFT:
                    lead_x_change = -movement_speed
                    lead_y_change = 0

                #Moving Right    
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = movement_speed
                    lead_y_change = 0

                #Moving Down
                elif event.key == pygame.K_DOWN:
                    lead_y_change = movement_speed
                    lead_x_change = 0

                #Moving Up
                elif event.key == pygame.K_UP:
                    lead_y_change = -movement_speed
                    lead_x_change = 0

        #Game Over When you touch the borders
        if lead_x > (display_width-27) or lead_x < 18 \
           or lead_y > (display_height-27) or lead_y < 18:
            gameOver = True
                     

            """If you want the object to stop moving when KEY IS UP"""
            #if event.type == pygame.KEYUP:
                #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                #event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    #lead_x_change = 0
                    #lead_y_change = 0
                    
        lead_x += lead_x_change
        lead_y += lead_y_change

        #Design Game With colours
        gameDisplay.fill(white)
        
        #Draws Rectangle
        #Apple
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])
        #Snake
        pygame.draw.rect(gameDisplay, black, [lead_x,lead_y,block_size,block_size])

        #Borders
        pygame.draw.rect(gameDisplay,black, [0,0,800,15])   #top
        pygame.draw.rect(gameDisplay,black, [0,0,15,600])   #left
        pygame.draw.rect(gameDisplay,black, [785,0,15,600]) #right
        pygame.draw.rect(gameDisplay,black, [0,585,800,15]) #bottom

  
        snakeHead = []
        snakeHead.append(lead_x)    #Append X Coordinate
        snakeHead.append(lead_y)    #Append Y Coordinate
        snakeList.append(snakeHead) #Append Coordinates to snakeList

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
        
        snake(block_size, snakeList)#Calling the Snake function to enlarge the snake
        
        pygame.display.update()

        #Overlap handling
        if lead_x == randAppleX and lead_y == randAppleY:
            print("nom nom nom")
            randAppleX = random.randrange(0,int(display_width-(29+block_size)),block_size)
            randAppleY = random.randrange(0,int(display_height-(29+block_size)), block_size)
            snakeLength += 1#Everytime the snake eats the apple,
                            #length of the snake increases
            score += 10
                                


        clock.tick(FPS)
                
        
    #Un-init the game
    pygame.quit()

    #Quits python
    quit()


gameLoop()
