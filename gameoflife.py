# Program relies on pygame library which can be found
# https://www.pygame.org/wiki/GettingStarted

import sys, pygame, random

#initialize pygame library
pygame.init()

#GAME MODIFIERS

WIDTH = 530 #Width of the pygame popup
            #grid is always WIDTH x WIDTH -> (WIDTH is used as height of grid)
HEIGHT = 680 #Height of pygame popup (should be approx 150pixels larger than WIDTH) 

#NUMBER OF ROWS AND COLUMNS MUST BE EQUAL
ROWS = 50 #number of rows in grid
COLS = 50 #number of columns in grid

LIFE_FREQUENCY = 0.3 #PROPORTION OF ALIVE CELLS in randomized generation(<=1)
SPEED = 1000 #number of ms between generations (default 1000 -> 1second)


#Base rules for conways game of life described here:
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
REVIVE = 3 #number of neighbours for a cell to come alive (or remain alive)
DEAD = 1 #number of neighbours for a cell to die (1 or 0)
STARVE = 4 #number of neighbours for a cell to starve (die) (4 or greater)

#GAME BOARD
SIZE = WIDTH, HEIGHT
BLACK = 0, 0, 0 #colour constant
WHITE = 255,255,255 #colour constant
RED = 255,0,0 #colour constant
GREEN = 0,255,0 #colour constant
ROWHEIGHT = (WIDTH-COLS-1)/ROWS #width (in pixels) of cells
COLWIDTH = (WIDTH-COLS-1)/COLS #height (in pixels) of cells
SCREEN = pygame.display.set_mode(SIZE) #pygame drawing surface initialization
GRID = [[0] * ROWS for i in range(COLS)] #active gameboard grid (int array)
NEW_GRID = [[0] * ROWS for i in range(COLS)] #temporary grid used when generating the next generation (int array)
ACTIVE_GAME = False #boolean for whether evolution is taking place currently
GEN = 0 #current generation number

#init title/header of pygame popup
pygame.display.set_caption('Conway\'s Game of Life')

#HELPER FUNCTIONS

#function randomly initializes the grid with values 0(dead) and 1(alive)
def randomInit():
    for x in range(ROWS):
        for y in range(COLS):
            GRID[x][y] = genState()#genState returns 0 or 1

#function returns 0 or 1 depending on the LIFE_FREQUENCY defined above
def genState():
    val = random.random()
    if val<LIFE_FREQUENCY:
        return 1
    else:
        return 0

#function draws the cells to the gameboard
def drawGrid():
    #X and Y coordinates of cells
    X = 1
    Y = 1
    #for loop iterators
    n = 0
    r = 0

    for n in range(ROWS):
        X = 1
        for r in range(COLS):
            if GRID[n][r] == 1:
                pygame.draw.rect(SCREEN,BLACK, [X,Y,COLWIDTH,ROWHEIGHT], border_radius=int(ROWHEIGHT/4))
            """ SECTION USED TO DRAW "DEAD" CELLS (if desired)
            else:
                pygame.draw.rect(SCREEN,RED, [X,Y,COLWIDTH,ROWHEIGHT], border_radius=int(ROWHEIGHT/4))
            """
            X += COLWIDTH+1
        Y+=ROWHEIGHT+1

#function calculates the next generation based on the rules of conways game of life
#
def nextGen():
    count = 0

    for x in range(ROWS):
        for y in range(COLS):
            count = 0
            #check number of neighbours
            if x-1>=0 and y-1>=0:#check top left
                if GRID[x-1][y-1] == 1:
                    count+=1
            if y-1>=0:#check top mid
                if GRID[x][y-1] == 1:
                    count+=1
            if x+1<COLS and y-1>=0:#check top right
                if GRID[x+1][y-1] == 1:
                    count+=1
            if x-1>=0:#check left
                if GRID[x-1][y] == 1:
                    count+=1
            if x+1<COLS:#check right
                if GRID[x+1][y] == 1:
                    count+=1
            if x-1>=0 and y+1<ROWS:#check bottom left
                if GRID[x-1][y+1] == 1:
                    count+=1
            if y+1<ROWS:#check bottom mid
                if GRID[x][y+1] == 1:
                    count+=1
            if x+1<COLS and y+1<ROWS:#check bottom right
                if GRID[x+1][y+1] == 1:
                    count+=1
            #based on the number of 'neighbours' counted, either revive, kill or leave cells the same
            if GRID[x][y] == 0 and count == REVIVE:
                NEW_GRID[x][y] = 1
            elif GRID[x][y] == 1 and (count<=DEAD or count>=STARVE):
                NEW_GRID[x][y] = 0
            else:
                NEW_GRID[x][y] = GRID[x][y]
    copyGrid()#function copies newly generated NEW_GRID to GRID
   
#function copies each cell from NEW_GRID to GRID   
def copyGrid():
    for x in range(ROWS):
        for y in range(COLS):
            GRID[x][y] = NEW_GRID[x][y]

#function updates and draws all text to the pygame popup
def updateText():
    #variables used to calculate vertical positioning of text
    VERTICAL = WIDTH #REMEMBER: width is the height of the gameboard
    SPACER = 15
    #variable used as horizontal spacer
    HORZ = 5

    #define the font for text, using default & size 21
    FONT = pygame.font.Font(None, 21)

    #text saying "Controls"
    controlsText = FONT.render('Controls:', True, BLACK) 
    controlsTextBox = controlsText.get_rect()
    controlsTextBox.midleft = (HORZ, VERTICAL)
    VERTICAL+=SPACER

    #text saying "Press 'r' to create a generation."
    randText = FONT.render('Press \'r\' to create a generation.', True, BLACK) 
    randTextBox = randText.get_rect()
    randTextBox.midleft = (HORZ, VERTICAL)
    VERTICAL+=SPACER

    #text saying "Press 's' to start/stop evolution."
    startStopText = FONT.render('Press \'s\' to start/stop evolution.', True, BLACK) 
    startStopTextBox = startStopText.get_rect()
    startStopTextBox.midleft = (HORZ, VERTICAL)
    VERTICAL+=SPACER

    #text saying "Press 'q' to quit."
    quitText = FONT.render('Press \'q\' to quit.', True, BLACK) 
    quitTextBox = quitText.get_rect()
    quitTextBox.midleft = (HORZ, VERTICAL)
    VERTICAL+=SPACER

    #text saying "Use up and down arrows to change evolution speed."
    speedModText = FONT.render('Use up and down arrows to change evolution speed.', True, BLACK) 
    speedModTextBox = speedModText.get_rect()
    speedModTextBox.midleft = (HORZ, VERTICAL)
    VERTICAL+=SPACER

    #text saying "Current Generation:" (and gen)
    numGenText = FONT.render('Current Generation: '+str(GEN), True, BLACK) 
    numGenTextBox = numGenText.get_rect()
    numGenTextBox.midleft = (HORZ, HEIGHT-SPACER)

    #text saying "Speed (Generations/Second):" (and speed)
    currSpeedText = FONT.render('Speed (Generations/Second): '+str(round(1000/SPEED,2)), True, BLACK) 
    currSpeedTextBox = currSpeedText.get_rect()
    currSpeedTextBox.midleft = (HORZ, HEIGHT-2*SPACER)

    #Drawing the dividing line seperating text from game
    pygame.draw.line(SCREEN, BLACK, (0,WIDTH), (WIDTH, WIDTH)) 
    #Display all text sections on gameboard
    SCREEN.blit(randText, randTextBox)
    SCREEN.blit(startStopText, startStopTextBox)
    SCREEN.blit(quitText, quitTextBox)
    SCREEN.blit(speedModText, speedModTextBox)
    SCREEN.blit(numGenText, numGenTextBox)
    SCREEN.blit(currSpeedText, currSpeedTextBox)

#ACTIVE PROGRAM
while 1:
    #checking for quitting the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        #Receive Keyboard Input
        if event.type == pygame.KEYDOWN:
            #Start/Stop Evolution
            if event.key == pygame.K_s:
                if ACTIVE_GAME:
                    ACTIVE_GAME = False
                else:
                    ACTIVE_GAME = True
            #Generate random gameboard
            if event.key == pygame.K_r:
                GEN = 0
                randomInit()
            #Quit the window
            if event.key == pygame.K_q:
                sys.exit()
            #Increase speed of evolution
            if event.key == pygame.K_UP:
                if SPEED>50:
                    SPEED-=50
            #Decrease speed of evolution
            if event.key == pygame.K_DOWN:
                if SPEED<5000:
                    SPEED+=50

   
    #IF ACTIVE_GAME : All updates occuring, Evolution is happening
    if ACTIVE_GAME: 
        SCREEN.fill(WHITE)
        drawGrid()
        nextGen()
        GEN+=1
        updateText()
        pygame.display.flip()
        pygame.time.delay(SPEED)
    else:#Minimum requirements for each call, no movement
        SCREEN.fill(WHITE)
        drawGrid()
        updateText()
        pygame.display.flip()

    

    



