import pickle


#Things to save
    #Position       -   pos
    #Money          -   money
    #Minerals       -   minerals
    #speed          -
    #fuel           -   fuel
    #Acceleration   -   player.dir
    #Direction
    #

#Current Values
pos = 1
money= 10
minerals = 1
fuel = 11

#File Name
savefile = 'save.p'

#List of Vars to save
GameVariables = [pos, money, minerals, fuel]

def saveGame():
    pickle.dump(GameVariables, open(savefile, 'wb'))
    

def loadGame():
    GameVariables = pickle.load(open(savefile, 'rb'))

saveGame()
loadGame()
    
    
    
    
    
    
