#!/usr/bin/python
import pygame, sys
from pygame.locals import *
import random

#Number of frames per second
FPS = 10
# set up the game window size
# def gameWindow():
WINDOWWIDTH = 640
GAMEHEIGHT = 450
MENUHEIGHT = 30
WINDOWHEIGHT = MENUHEIGHT + GAMEHEIGHT

# set up the cell size, and number
CELLSIZE = 10
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert GAMEHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"
CELLWIDTH = WINDOWWIDTH / CELLSIZE # number of cells wide
CELLHEIGHT = GAMEHEIGHT / CELLSIZE # Number of cells high

# set up the colours
BLACK =    (0,0,0)
WHITE =    (255,255,255)
DARKGRAY = (40,40,40)
GREEN =    (0,255,0)

#Draws the grid lines
def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0),(x,GAMEHEIGHT))
    for y in range(0, GAMEHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0,y), (WINDOWWIDTH, y))

#Blanking the grid
def blankGrid():
    gridDict = {}
    for y in range (CELLHEIGHT):
        for x in range (CELLWIDTH):
            gridDict[x,y] = 0
    return gridDict
    
####################################################################################################################
#                                       The Different Starting possibilities                                       #
####################################################################################################################

#Filling the grid with life
def startingGridRandom(lifeDict):
    #Random
    pygame.display.set_caption('Conway\'s Game of Life: Random')
    for item in lifeDict:
        lifeDict[item] = random.randint(0,1)
    return lifeDict

#Setting one R-pentomino at Start
def startingRpentomino(lifeDict):
    #R-pentomino
    pygame.display.set_caption('Conway\'s Game of Life: R-pentomino')
    lifeDict[48,32] = 1
    lifeDict[49,32] = 1
    lifeDict[47,33] = 1
    lifeDict[48,33] = 1
    lifeDict[48,34] = 1
    return lifeDict

#Setting one Acorn at Start
def startingAcorn(lifeDict):
    #Acorn
    pygame.display.set_caption('Conway\'s Game of Life: Acorn')
    lifeDict[105,55] = 1
    lifeDict[106,55] = 1
    lifeDict[109,55] = 1
    lifeDict[110,55] = 1
    lifeDict[111,55] = 1
    lifeDict[106,53] = 1
    lifeDict[108,54] = 1
    return lifeDict
    
def startingDiehard(lifeDict):
    #Diehard
    pygame.display.set_caption('Conway\'s Game of Life: Diehard')
    lifeDict[45,45] = 1
    lifeDict[46,45] = 1
    lifeDict[46,46] = 1
    lifeDict[50,46] = 1
    lifeDict[51,46] = 1
    lifeDict[52,46] = 1
    lifeDict[51,44] = 1
    return lifeDict

def startingGosperGliderGun(lifeDict):
    #Gosper Glider Gun
    pygame.display.set_caption('Conway\'s Game of Life: Gosper\'s Glider Gun')

    #left square
    lifeDict[14,15] = 1
    lifeDict[14,16] = 1
    lifeDict[15,15] = 1
    lifeDict[15,16] = 1

    #left part of gun
    lifeDict[24,15] = 1
    lifeDict[24,16] = 1
    lifeDict[24,17] = 1
    lifeDict[25,14] = 1
    lifeDict[25,18] = 1
    lifeDict[26,13] = 1
    lifeDict[27,13] = 1
    lifeDict[26,19] = 1
    lifeDict[27,19] = 1
    lifeDict[28,16] = 1
    lifeDict[29,14] = 1
    lifeDict[29,18] = 1
    lifeDict[30,15] = 1
    lifeDict[30,16] = 1
    lifeDict[30,17] = 1
    lifeDict[31,16] = 1

    #right part of gun
    lifeDict[34,13] = 1
    lifeDict[34,14] = 1
    lifeDict[34,15] = 1
    lifeDict[35,13] = 1
    lifeDict[35,14] = 1
    lifeDict[35,15] = 1
    lifeDict[36,12] = 1
    lifeDict[36,16] = 1
    lifeDict[38,11] = 1
    lifeDict[38,12] = 1
    lifeDict[38,16] = 1
    lifeDict[38,17] = 1

    #right square
    lifeDict[48,13] = 1
    lifeDict[48,14] = 1
    lifeDict[49,13] = 1
    lifeDict[49,14] = 1

    return lifeDict
    
####################################################################################################################
        
#Adding some colour to the life
def colourGrid(item, lifeDict):
    x = item[0]
    y = item[1]
    y = y * CELLSIZE # translates array into grid size
    x = x * CELLSIZE # translates array into grid size
    if lifeDict[item] == 0:
        pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, CELLSIZE, CELLSIZE))
    if lifeDict[item] == 1:
        pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, CELLSIZE, CELLSIZE))
    return None

def getNeighbours(item,lifeDict):
    neighbours = 0
    for x in range (-1,2):
        for y in range (-1,2):
            checkCell = (item[0]+x,item[1]+y)
            if checkCell[0] < CELLWIDTH  and checkCell[0] >=0:
                if checkCell [1] < CELLHEIGHT and checkCell[1]>= 0:
	            if lifeDict[checkCell] == 1:
                        if x == 0 and y == 0:
                            neighbours += 0
                        else:
                            neighbours += 1
    return neighbours    
        
def tick(lifeDict):
    newTick = {}
    for item in lifeDict:
        numberNeighbours = getNeighbours(item, lifeDict)
	if lifeDict[item] == 1: # For those cells already alive
            if numberNeighbours < 2: # kill under-population
                newTick[item] = 0
            elif numberNeighbours > 3: #kill over-population
                newTick[item] = 0
            else:
                newTick[item] = 1 # keep status quo (life)
        elif lifeDict[item] == 0:
            if numberNeighbours == 3: # cell reproduces
                newTick[item] = 1
            else:
                newTick[item] = 0 # keep status quo (death)                
    return newTick                
                
####################################################################################################################

def main():
#setting up the board
    pygame.init()
    global DISPLAYSURF
    myFont = pygame.font.SysFont("monospace", 15)
    generation = 0
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    DISPLAYSURF.fill(WHITE) #fills the screen white
    lifeDict = blankGrid() # creates library and populates to match blank grid
#Running the game
# Starting options
# This needs to be in a menu!
#    lifeDict = startingGridRandom(lifeDict) # Assign random life
#    lifeDict = startingRpentomino(lifeDict) # Setup R-pentomino
#    lifeDict = startingAcorn(lifeDict) # Setup Acorn
#    lifeDict = startingDiehard(lifeDict) # Setup DieHard
    lifeDict = startingGosperGliderGun(lifeDict) # Setup Gosper's Glider Gun

########################################################################################
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        lifeDict = tick(lifeDict) #runs a tick
        DISPLAYSURF.fill(WHITE)
        for item in lifeDict:
            colourGrid(item, lifeDict) #Colours the live cells, blanks the dead

        # here is where the score is kept/displayed.
        scoretext = myFont.render("Generation: {0}".format(generation), 1, (0,0,0))
        DISPLAYSURF.blit(scoretext, (5, 455))
        generation += 1
        drawGrid()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()
