# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
# Converted for AstroPi - Fergus and Raymond Lesley 31 may 2015

import random, pygame, sys
from pygame.locals import *
from astro_pi import AstroPi

FPS = 1.0    # game speed in Frames Per Second
ACCEL = 0.1  # speed increase per apple
WINDOWWIDTH = 8
WINDOWHEIGHT = 8
CELLSIZE = 1
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
OFFSCREEN = {'x': -100, 'y': -100}

#             R    G    B
WHITE     = ( 63,  63,  63)
BLACK     = (  0,   0,   0)
RED       = (127,   0,   0)
GREEN     = (  0, 127,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
YELLOW    = (255, 255,   0)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

# High score
hiscore = 0
ap = AstroPi()
# ap.set_rotation(180, True)

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_mode((640, 480))  # needed for pygame events

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    # Set a random start point.
    xgap = WINDOWWIDTH / 2
    ygap = WINDOWHEIGHT / 2
    startx = random.randint(xgap-1, WINDOWWIDTH - xgap)
    starty = random.randint(ygap-1, WINDOWHEIGHT - ygap)
    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty}]
    direction = RIGHT

    # game parameters
    speed = FPS
    global hiscore

    # Start the apple in a random place.
    apple = getRandomLocation()
    nom = OFFSCREEN
    nomcounter = 0

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # remember apple location for nom message
            nom = apple
            nomcounter = speed
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
            # and go faster!
            speed = speed + ACCEL
        else:
            del wormCoords[-1] # remove worm's tail segment
            # process "nom" timer
            if nomcounter <= 0:
                # timer expired - remove "Nom!"
                nom = OFFSCREEN
            else:
                nomcounter = nomcounter - 1

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0, newHead)
        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        score = len(wormCoords) - 3
        if score > hiscore:
            hiscore = score
        # DISPLAYSURF.fill(BGCOLOR)
        ap.clear()
        drawWorm(wormCoords)
        drawApple(apple)
        pygame.display.update()
        FPSCLOCK.tick(speed)


# KRT 14/06/2012 rewrite event detection to deal with mouse use
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:      #event is quit 
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:   #event is escape key
                terminate()
            else:
                return event.key   #key found return with it
    # no quit or key events in queue so return None    
    return None

    
def showStartScreen():
    pygame.event.get()  #clear out event queue

    print("Press a key to begin...")
    while True:
        # ap.show_message("Press a key to play")
        ap.show_message("<>", 0.1, WHITE)
        if checkForKeyPress():
            return

def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    pygame.event.get()  #clear out event queue 

    print("Game Over! :(")
    while True:
        ap.show_message("><", 0.01, WHITE)
        if checkForKeyPress():
            return
#KRT 12/06/2012 reduce processor loading in gameover screen.
        pygame.time.wait(100)

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        ap.set_pixel(x , y , GREEN)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    ap.set_pixel(x, y, RED)


if __name__ == '__main__':
    main()
