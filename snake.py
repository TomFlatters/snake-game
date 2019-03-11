import pygame
import random
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((640,480)) #sets the window size
pygame.display.set_caption('Snake') #sets the title bar
pygame.mouse.set_visible(0)

clock = pygame.time.Clock() # get a clock for the main loop
running = True # should the game stop?

up = 0 # directions
right = 1
down = 2
left = 3

snakePos = [(16,12)]
snakeDir = 4
length = 1 # how long the snake is
myfont = pygame.font.SysFont("monospace", 16)

# Add Fruit
fruitPos = [(random.randrange(1,32),random.randrange(1,24))]


gridSize = (32,24)  # size of game grid

updateInvFreq = 5   # how many frames it takes for the game to update

snakeSquare = pygame.Surface((20,20)) # define a rectangle
snakeSquare.fill(pygame.Color("red")) # color it in

fruitSquare = pygame.Surface((20,20))
fruitSquare.fill(pygame.Color("blue"))

background = pygame.Surface((640,480))
background.fill(pygame.Color("black"))

def handleEvents():
    global snakeDir # need to modify snake direction
    global running  # same here

    for event in pygame.event.get():
        if event.type == QUIT:  # quit if we press close
            running = False
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
        elif event.type == KEYDOWN and event.key == K_LEFT:
            snakeDir = left
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            snakeDir = right
        elif event.type == KEYDOWN and event.key == K_UP:
            snakeDir = up
        elif event.type == KEYDOWN and event.key == K_DOWN:
            snakeDir = down

def update():
    global snakePos
    global fruitPos
    global running
    global length

    (x,y) = snakePos[0] # get first snake position and update it
    if snakeDir == up:
        y = (y-1) % gridSize[1]
    elif snakeDir == down:
        y = (y+1) % gridSize[1]
    elif snakeDir == left:
        x = (x-1) % gridSize[0]
    elif snakeDir == right:
        x = (x+1) % gridSize[0]
    elif snakeDir == 4:
        pass
    else:
        raise Exception(
            "The direction of the snake isn't valid: " + 
            str(snakeDir)
        )

    snakePos.insert(0, (x,y)) # add new position to the snake

    # longer snakes and add fruit logic
    if (snakePos[0] == fruitPos[0]):
        length += 1
        fruitPos = [(random.randrange(1,32),random.randrange(1,24))]
    elif (snakePos[0] in snakePos[1:]):
        snakePos = [(x,y)]
        length = 1
    else:
        snakePos.pop() #remove old one so doesn't grow



def draw():
    screen.blit(background, (0,0)) # clear the screen with the black rectangle

    # draw fruit
    screen.blit(fruitSquare, ((fruitPos[0][0] * 20), (fruitPos[0][1] * 20)))

    # draw the snake blocks
    # remember to multiply positions by the size of a block
    for i in range(0,len(snakePos)):
        screen.blit(snakeSquare, ((snakePos[i][0] * 20), (snakePos[i][1] * 20)))

    # update
    scoretext = myfont.render("Score = "+str(length-1), True, (255,255,255))
    screen.blit(scoretext, (5, 10))

    # and flip the screen
    pygame.display.flip()

# how many frames have passed since last update?
updateCounter = 0

# WE NEED A GAME LOOP TO KEEP THE WINDOW OPEN, THIS IS JUST AN EXAMPLE:
while running:
    # sync game with display
    clock.tick(60)
    # get events to update with
    handleEvents()


    # if enough frames have passed, update
    if (updateCounter == 0):
        update()

    # redraw everything
    draw()
    updateCounter = (updateCounter + 1) % updateInvFreq

pygame.quit()
