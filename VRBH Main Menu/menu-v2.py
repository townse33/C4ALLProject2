import pygame, sys


class Option():

    hovered = False
    
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        
        
        self.set_rect() #call set_rect function

       
        self.draw()  #call draw function
            
    def draw(self):
        self.set_rend()
        screen.blit(self.rend, self.rect) #blits text into correct position
        
    def set_rend(self):
        #Renders text with correct colour
        self.rend = menu_font.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (100, 100, 100) #text colour is grey when hovered over
        else:
            return (255, 255, 255) #text colour is white when NOT hovered over
        
    def set_rect(self):
        self.set_rend() #call set_rend function
        self.rect = self.rend.get_rect() #equal to rectangular co-ordinates of text
        self.rect.topleft = self.pos #top left co-ordinate is equal to position of text


#class Clicked(Option):
#    def __init__(self):
#        self.option1()
    
#    def option1(self):
#        if option.rect.collidepoint(pygame.mouse.get_pos()):
#            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                print("work")

#initializes pygame
pygame.init()

#sets screen size to 1200x800
screen = pygame.display.set_mode((1200, 800))

#sets font style and size
menu_font = pygame.font.Font(None, 40)
title_font = pygame.font.Font(None, 80)

#creates title
title = title_font.render("VRBH GAME", True, (255, 255, 255))

#calls the 'Option' class with three objects

option1 = Option("NEW GAME", (515, 350))
option2 = Option("LEADERBOARDS", (480, 400))
option3 = Option("QUIT", (563, 450))

#loads background image and converts it
bg = pygame.image.load("background.jpg").convert()

a = True
#main loop
while a == True:
    pygame.event.pump()
    screen.blit(bg,(0, 0)) #Blits background to screen
    screen.blit(title, (425, 15)) #Blits title to screen

    #if the mouse 'collides' with the text, hovered will be equal to True
    for option in option1, option2, option3:
        if option.rect.collidepoint(pygame.mouse.get_pos()):
            option.hovered = True
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if option1.rect.collidepoint(pygame.mouse.get_pos()) == True:
                        print("(this will start the game)")
                    elif option2.rect.collidepoint(pygame.mouse.get_pos()) == True:
                        print(execfile("script2.py")
)
                    else:
                        a = False
                    
        else:
            option.hovered = False
        option.draw()
 #   Clicked()
    pygame.display.update()

pygame.quit()  
sys.exit()
