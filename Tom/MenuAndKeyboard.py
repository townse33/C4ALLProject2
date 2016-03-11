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

#creates titles
title = title_font.render("STAR HUNT", True, (255, 255, 255))
title2 = title_font.render("Keyboard Controls", True, (255, 255, 255))
#calls the 'Option' class with three objects

option1 = Option("NEW GAME", (515, 350))
option2 = Option("LEADERBOARDS", (480, 400))
option3 = Option("QUIT", (563, 450))
option4 = Option("RESUME GAME", (515,350))
option4 = Option("Keyboard Controls", (10,770))

#Keyboard Shortcut Options - calls the 'Option' class with these objects
option5 = Option("Back to Menu", (520, 750))
option0 = Option(" ", (0,0))

option6 = Option("W  -  Move Forward ", (200,200))
option7 = Option("A  -  Rotate Left ", (200,250))
option8 = Option("S  -  Slow Down ", (200,300))
option9 = Option("D  -  Rotate Right ", (200,350))
option10 = Option("Q  -  Quit Game", (200,400))
option11 = Option("Esc  -  Pause Menu", (200,450))
option12 = Option("M  -  Mine", (200,500))
option13 = Option("Left CTRL + Z  -  Back to Menu", (200,550))

keyboardControls = [option6, option7, option8, option9, option10, option11, option12, option13]
#loads background image and converts it
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
        if pressed[pygame.K_q]:
            loop  = False


              #if mouse 'collides' with text, mouseHover will be True
        for option in option5, option0:
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

        for option in keyboardControls:
            option.draw()




        pygame.display.update()



def xfile(afile, globalz=None, localz=None):
    with open(afile, "r") as fh:
        exec(fh.read(), globalz, localz)
        
def mainMenu():
    #main loop
    loop = True
    while loop == True:
        pygame.event.pump() #Internally process pygame vent handlers
        screen.blit(bg,(0, 0)) #Blits background to screen
        screen.blit(title, (425, 15)) #Blits title to screen

        pressed = pygame.key.get_pressed() #Variable for when keys are held down

        if pressed[pygame.K_q]:
            loop  = False

        #if the mouse 'collides' with the text, hovered will be equal to True
        for option in option1, option2, option3, option4:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.mouseHover = True
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if option1.rect.collidepoint(pygame.mouse.get_pos()) == True:
                            import MainWithSpeed
                        elif option2.rect.collidepoint(pygame.mouse.get_pos()) == True:
                            print(execfile("script2.py"))
                        elif option4.rect.collidepoint(pygame.mouse.get_pos()) == True: #'Keyboard Shortcuts' clicked on
                            loop = False
                            shortcutKeys()
                        else:
                            loop = False
                    
            else:
                option.mouseHover= False
            option.draw()

        pygame.display.update()

def pauseMenu():
    loop = True
    while loop == True:
        pygame.event.pump()
        screen.blit(bg, (0,0))
        screen.blit(title, (425,15))

        for option in option3, option4:
            if option.rect.collidepoint(pygame.mouse.get_pos()):
                option.mouseHover = True
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if option4.rect.collidepoint(pygame.mouse.get_pos()) == True:
                            pass
                        elif option3.rect.collidepoint(pygame.mouse.get_pos()) == True:
                            pygame.quit()
                        else:
                            loop = False
            else:
                option.mouseHover = False
            option.draw()

        pygame.display.update()

mainMenu()
pygame.quit()  
sys.exit()
