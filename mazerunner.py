"""Maze runner game"""
import pygame

#Setting colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

class Wall(pygame.sprite.Sprite):
    

    def __init__(self, x, y, width, height, color):
        #call parents constructor
        super().__init__()

        #make a wall of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        #make our top-left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

class Player(pygame.sprite.Sprite):
        """This class represents the bar at the bottom that the player will control"""

        #set speet vector
        change_x = 0
        change_y = 0

        def __init__(self, x, y):
            #call parents constructor
            super().__init__()

            #set height, width
            self.image = pygame.image.load("stand_down.png")
            self.image = self.image.convert_alpha()
            

            #make top-left corner the passed-in location
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x

        def changespeed(self, x, y):
            """ Change the speed of the player. Called with a keypress. """
            self.change_x += x
            self.change_y += y

        def move(self, walls):
            """ Find a new position for the player """

            #move left/right
            self.rect.x += self.change_x

            #check if the update caused us to hit a wall
            block_hit_list = pygame.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:
                #if we are moving right, set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                else:
                    #otherwise we are moving left so do the opposite
                    self.rect.left = block.rect.right

            #move up/down
            self.rect.y += self.change_y

            #check if the update caused us to hit a wall
            block_hit_list = pygame.sprite.spritecollide(self, walls, False)
            for block in block_hit_list:

                #reset position based on the top/bottom of the object
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                else:
                    self.rect.top = block.rect.bottom

class Room(object):
    """base class for all rooms."""

    #each room has a list of walls
    wall_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()

class Room1(Room):
    """This creates all walls in room 1"""
    def __init__(self):
        super().__init__()

        #list of walls. All in form [x, y, width, height]
        walls = [[0, 0, 20, 250, WHITE],
                 [0, 350, 20, 250, WHITE],
                 [780, 0, 20, 250, WHITE],
                 [780, 350, 20, 250, WHITE],
                 [20, 0, 760, 20, WHITE],
                 [20, 580, 760, 20, WHITE],
                 [390, 130, 20, 450, BLUE]
                 ]

        #loop through list, create wall, and add to list
        for i in walls:
            wall = Wall(i[0], i[1], i[2], i[3], i[4])
            self.wall_list.add(wall)

#next rooms are almost identical to the first
class Room2(Room):
    """This creates all walls in room 2"""
    def __init__(self):
        super().__init__()

        #list of walls. All in form [x, y, width, height]
        walls = [[0, 0, 20, 250, RED],
                 [0, 350, 20, 250, RED],
                 [780, 0, 20, 250, RED],
                 [780, 350, 20, 250, RED],
                 [20, 0, 760, 20, RED],
                 [20, 580, 760, 20, RED],
                 [190, 20, 20, 400, GREEN],
                 [590, 180, 20, 400, GREEN]
                 ]

        #loop through list, create wall, and add to list
        for i in walls:
            wall = Wall(i[0], i[1], i[2], i[3], i[4])
            self.wall_list.add(wall)

class Room3(Room):
    """This creates all walls in room 3"""
    def __init__(self):
        super().__init__()

        #list of walls. All in form [x, y, width, height]
        walls = [[0, 0, 20, 250, PURPLE],
                 [0, 350, 20, 250, PURPLE],
                 [780, 0, 20, 250, PURPLE],
                 [780, 350, 20, 250, PURPLE],
                 [20, 0, 760, 20, PURPLE],
                 [20, 580, 760, 20, PURPLE]
                 ]

        #loop through list, create wall, and add to list
        for i in walls:
            wall = Wall(i[0], i[1], i[2], i[3], i[4])
            self.wall_list.add(wall)

        for x in range(100, 800, 100):
            for y in range(50, 451, 300):
                wall = Wall(x, y, 20, 200, RED)
                self.wall_list.add(wall)

def main():
    """main program"""

    #call this function so the Pygame library can initialize itself
    pygame.init()

    #create an 800x600 screen
    screen = pygame.display.set_mode([800, 600])

    #title of window
    pygame.display.set_caption('Maze Running Game')

    #create player paddle object
    player = Player(50, 50)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    rooms = []

    room = Room1()
    rooms.append(room)

    room = Room2()
    rooms.append(room)

    room = Room3()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    clock = pygame.time.Clock()

    done = False

    while not done:
        #keyboard activity processing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(5,0)
                if event.key == pygame.K_UP:
                    player.changespeed(0,-5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 5)

            #evens it out so the current location will be (0,0) after input

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(5,0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -5)

        #changing room based on location on screen

        player.move(current_room.wall_list)

        if player.rect.x < -15:
            if current_room_no == 0:
                current_room_no = 2
                current_room = rooms[current_room_no]
                player.rect.x = 790
            elif current_room_no == 2:
                current_room_no = 1
                current_room = rooms[current_room_no]
                player.rect.x = 790
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.x = 790


        if player.rect.x > 801:
            if current_room_no == 0:
                current_room_no = 1
                current_room = rooms[current_room_no]
                player.rect.x = 0
            elif current_room_no == 1:
                current_room_no = 2
                current_room = rooms[current_room_no]
                player.rect.x = 0
            else:
                current_room_no = 0
                current_room = rooms[current_room_no]
                player.rect.x = 0

        #drawing
        screen.fill(BLACK)

        movingsprites.draw(screen)
        current_room.wall_list.draw(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
                    


