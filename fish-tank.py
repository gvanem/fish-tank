import curses
import random
import time
import sys
from curses import wrapper

bubbleCoordinates = [[0 for x in range(2)] for y in range(10)]
kelpCoordinates = [[0 for x in range(2)] for y in range(6)]
fishCoordinates = [[0 for x in range(2)] for y in range(6)]

def main(stdscr):
    init_arrays()
    curses.curs_set(False)
    # Initialize curses
    init_curses_color(stdscr)
    exit = False
    while not exit:
        stdscr.clear()
        #draw fish tank
        draw_fish_tank(stdscr)
        #draw kelp
        draw_kelp(stdscr)
        #update and draw bubbles (up up and up)
        draw_bubbles(stdscr)
        #update and draw fish
        draw_fish(stdscr)
        stdscr.refresh()
        stdscr.nodelay(True)
        key = stdscr.getch()
        if key == ord('q'):
            exit = True
        time.sleep(0.25)

    
def init_curses_color(stdscr):
    curses.use_default_colors()
    if sys.platform != 'win32':
        for i in range(0, curses.COLORS):
            curses.init_pair(i, i, -1)

def draw_fish_tank(stdscr):
    # Draw left and right side
    for i in range(0, curses.LINES - 1):
        if i == (curses.LINES - 2):
            stdscr.addch(i, 0, curses.ACS_LLCORNER)
            stdscr.addch(i, curses.COLS - 1, curses.ACS_LRCORNER)
        else:
            stdscr.addch(i, 0, curses.ACS_VLINE)
            stdscr.addch(i, curses.COLS - 1, curses.ACS_VLINE)
    # Draw top and bottom
    for i in range(1 , curses.COLS - 1):
        stdscr.addstr(0, i, '~', curses.color_pair(6))
        stdscr.addch(curses.LINES - 2, i, curses.ACS_HLINE)
        stdscr.addstr(curses.LINES - 1, 0, '[q]uit')

def draw_kelp(stdscr):
    for i in range(6):
        for j in range(kelpCoordinates[i][1]):
            stdscr.addstr(curses.LINES - 3 - j, kelpCoordinates[i][0], '#', curses.color_pair(2))

def draw_bubbles(stdscr):
    # update position (decrease y by 1)
    for i in range(10):
        bubbleCoordinates[i][1] = bubbleCoordinates[i][1] - 1
        # check if any bubbles have gone off the screen, if so, bring it back down to the bottom
        if bubbleCoordinates[i][1] < 1:
            bubbleCoordinates[i][0] = random.randint(1, curses.COLS - 2)
            bubbleCoordinates[i][1] = curses.LINES - 3
        # draw bubbles
        stdscr.addstr(bubbleCoordinates[i][1], bubbleCoordinates[i][0], '.', curses.color_pair(6))

def draw_fish(stdscr):
    # Update position. If position went to the right, draw to the right. If left, go to left.
    for i in range(6):
        x = random.randint(-1, 1)
        y = random.randint(-1, 1)
        fishCoordinates[i][0] = fishCoordinates[i][0] + x
        if fishCoordinates[i][0] < 1:
            fishCoordinates[i][0] = 1
        elif fishCoordinates[i][0] > curses.COLS - 2:
            fishCoordinates[i][0] = curses.COLS - 2
        fishCoordinates[i][1] = fishCoordinates[i][1] + y
        if fishCoordinates[i][1] < 1:
            fishCoordinates[i][1] = 1
        elif fishCoordinates[i][1] > curses.LINES - 4:
            fishCoordinates[i][1] = curses.LINES - 4
        # If x is -1, the fish went to the left, else it went to the right
        if x == -1:
            stdscr.addstr(fishCoordinates[i][1], fishCoordinates[i][0], '0<')
        else:
            stdscr.addstr(fishCoordinates[i][1], fishCoordinates[i][0], '>0')


def init_arrays():
    # Initialize kelp position and height and randomize fish position
    for i in range(6):
        kelpCoordinates[i][0] = random.randint(1, curses.COLS - 2)
        kelpCoordinates[i][1] = random.randint(3, curses.LINES - 8)
        fishCoordinates[i][0] = random.randint(1, curses.COLS - 2)
        fishCoordinates[i][1] = random.randint(3, curses.LINES - 2)
    # Initialize bubble position
    for i in range(10):
        bubbleCoordinates[i][0] = random.randint(1, curses.COLS - 2)
        bubbleCoordinates[i][1] = random.randint(1, curses.LINES - 3)
wrapper(main)
