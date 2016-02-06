from tkinter import *

import sys
            
root = Tk()
root.geometry('{}x{}'.format(1400,900))

#Frames
class rightFrame():
    def __init__(self):
        self.rFrame = Frame(root, bg = "black", width = 200)
        self.rFrame.pack(side = RIGHT)

        
class gameFrame():
    def __init__(self):
        self.gFrame = Frame(root)
        self.gFrame.pack(side = LEFT)
        

class quitButton():
    def __init__(self):
        self.qButton = Button(self.rFrame, text = 'Quit', fg = 'red', command = self.quitProgram)
        self.qButton.pack()

    def quitProgram(self):
        root.destroy()



class mainMenu():
    pass






right_Frame = rightFrame()
game_Frame = gameFrame()
quitB = quitButton()



root.mainloop()


