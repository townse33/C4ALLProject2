import pygame, sys


class Option():
    
    #Variable to store wether text is hovered over or not
    mouseHover = False

    
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        
        
        self.set_rect() #call set_rect function
        self.draw()  #call draw function
            
    def draw(self):
        self.set_rend() #call set_rend function
        screen.blit(self.rend, self.rect) #blits text into correct position
        
    def set_rend(self):
        #Renders text with correct colour
        self.rend = menu_font.render(self.text, True, self.colour_choice())
        
    def colour_choice(self):
        if self.mouseHover:
            return (100, 100, 100) #text colour is grey when hovered over
        else:
            return (255, 255, 255) #text colour is white when NOT hovered over
        
    def set_rect(self):
        self.set_rend() #call set_rend function
        self.rect = self.rend.get_rect() #equal to rectangular co-ordinates of text
        self.rect.topleft = self.pos #top left co-ordinate is equal to position of text


#initializes pygame
pygame.init()

#sets screen size to 1200x800
screen = pygame.display.set_mode((1200, 800))

#sets font style and size
menu_font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 80)

#creates game titles
title = title_font.render("STAR HUNT", True, (255, 255, 255))
title2 = title_font.render("Keyboard Shortcuts", True, (255, 255, 255))
#Main Menu Options - calls the 'Option' class with these objects
option1 = Option("NEW GAME", (515, 350))
option2 = Option("LEADERBOARDS", (480, 400))
option3 = Option("QUIT", (563, 450))
option4 = Option("Keyboard Shortcuts", (10,770))
#Keyboard Shortcut Options - calls the 'Option' class with these objects
option5 = Option("Back to Menu", (520, 750))
option6 = Option(" ", (0,0))
option7 = Option("Left CTRL + Q  -  Quit Game", (200,200))
option8 = Option("Left CTRL + M  -  Back to Menu", (200,250))
#loads background image and converts it (for quicker rendering)
bg = pygame.image.load("background.jpg").convert()



def shortcutKeys():
    #main loop
    loop = True
    while loop == True:
        pygame.event.pump() #Internally process pygame event handlers
        screen.blit(bg,(0, 0)) #Blits background to screen
        screen.blit(title2, (325, 15)) #Blits title to screen
        

        pressed = pygame.key.get_pressed() #Variable for when keys are held down

        #if keys are LCTRL and Q then Quit game
        if pressed[pygame.K_LCTRL] and pressed[pygame.K_q]:
            loop  = False


              #if mouse 'collides' with text, mouseHover will be True
        for option in option5, option6:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.mouseHover = True
                for event in pygame.event.get():
                       
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #left mouse button clicked
                        if option5.rect.collidepoint(pygame.mouse.get_pos()) == True: #'new game' clicked on
                            loop = False
                            mainMenu()

            else:
                option.mouseHover = False
            option.draw()

        for option in option7, option8:
            option.draw()




        pygame.display.update()


def mainMenu():
    #main loop
    loop = True
    while loop == True:
        pygame.event.pump() #Internally process pygame event handlers
        screen.blit(bg,(0, 0)) #Blits background to screen
        screen.blit(title, (425, 15)) #Blits title to screen
        

        pressed = pygame.key.get_pressed() #Variable for when keys are held down
        
        #if keys are LCTRL and Q then Quit game
        if pressed[pygame.K_LCTRL] and pressed[pygame.K_q]:
            loop  = False
      





        #if mouse 'collides' with text, mouseHover will be True
        for option in option1, option2, option3, option4:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.mouseHover = True
                for event in pygame.event.get():
                       
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #left mouse button clicked
                        if option1.rect.collidepoint(pygame.mouse.get_pos()) == True: #'new game' clicked on
                            print("This will start a new game")
                        elif option2.rect.collidepoint(pygame.mouse.get_pos()) == True: #'leaderboards' clicked on
                            print(execfile("script2.py"))
                        elif option4.rect.collidepoint(pygame.mouse.get_pos()) == True: #'Keyboard Shortcuts' clicked on
                            loop = False
                            shortcutKeys()
                        else: #'quit' clicked on
                           loop = False
                
                
            
                    
            else:
                option.mouseHover = False
            option.draw()

        pygame.display.update()





mainMenu()
pygame.quit()  
sys.exit()
