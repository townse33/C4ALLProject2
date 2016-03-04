import pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1200,800))
bg = pygame.image.load("background.jpg")
   

class GameMenu():
    def __init__(self, screen, items, font=None, font_size=30, font_color=(255, 255, 255)):
 
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
        self.clock = pygame.time.Clock()
        self.items = items
        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color
        self.items = []
        #Creates a counter for an iterable
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
 
            width = label.get_rect().width
            height = label.get_rect().height
            #X position
            posx = (self.scr_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            #Y position
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
            #Appends to the list 'items'
            self.items.append([item,label, (width, height), (posx, posy)])

      
 
    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 60 FPS
            self.clock.tick(60)
            #If python is quitted
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
 
            # Redraw the background
            self.screen.blit(bg,(0,0))
            pygame.display.flip()

            #Draw menu options
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))

    

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((1200,800))
    pygame.display.set_caption('Space Game Menu Screen')
    menu_items = ('Start', 'Leaderboards', 'Exit')
    gm = GameMenu(screen, menu_items)
    gm.run()

    
