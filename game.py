# importing the required libraries
import pygame as pg
import sys
import time
from pygame.locals import *
from algorithms.neural_network import NeuralNetwork

# declaring the global variables

cpu = NeuralNetwork()

# for storing the 'x' or 'o'
# value as character
XO = 1 # represents 'X'
N = 5

# storing the winner's value at
# any instant of code
winner = None

# to check if the game is a draw
draw = None

# to set width of the game window
width = 500

# to set height of the game window
height = 500

# to set background color of the
# game window
white = (255, 255, 255)

# color of the straight lines on that
# white game board, dividing board
# into 9 parts
line_color = (0, 0, 0)

# setting up a 3 * 3 board in canvas
board = [[None] * N for _ in range(N)]

# initializing the pygame window
pg.init()

# setting fps manually
fps = 30

# this is used to track time
CLOCK = pg.time.Clock()

# this method is used to build the
# infrastructure of the display
screen = pg.display.set_mode((width, height + 100), 0, 32)

# setting up a nametag for the
# game window
pg.display.set_caption("Tic Tac Toe")

# loading the images as python object
initiating_window = pg.image.load("assets/modified_cover.png")
x_img = pg.image.load("assets/X_modified.png")
y_img = pg.image.load("assets/o_modified.png")

# resizing images
initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (32000 // width, 32000 // height))
o_img = pg.transform.scale(y_img, (32000 // width, 32000 // height))


cpu.feed_forward([0]*25) # works i think?


def game_initiating_window():
    # displaying over the screen
    screen.blit(initiating_window, (0, 0))

    # updating the display
    pg.display.update()
    time.sleep(3)
    screen.fill(white)

    # drawing vertical lines
    for i in range(1, N):
        pg.draw.line(screen, line_color, (width / N * i, 0), (width / N * i, height), 7)

    # drawing horizontal lines
    for i in range(1, N):
        pg.draw.line(screen, line_color, (0, height / N * i), (width, height / N * i), 7)

    draw_status()


def draw_status():
    # getting the global variable draw
    # into action
    global draw

    if winner is None: message = ("X" if XO else "O") + "'s Turn"
    else: message = winner.upper() + " won !"
    if draw: message = "Game Draw !"

    # setting a font object
    font = pg.font.Font(None, 30)

    # setting the font properties like
    # color and width of the text
    text = font.render(message, 1, (255, 255, 255))

    # copy the rendered message onto the board
    # creating a small block at the bottom of the main display
    screen.fill((0, 0, 0), (0, height, height + 100, 100))
    text_rect = text.get_rect(center=(width / 2, height + 50))
    screen.blit(text, text_rect)
    pg.display.update()


def check_win():
    global board, winner, draw

    # checking for winning rows
    for row in range(0, N):
        l = board[row]
        if (len(set(l[:-1])) == 1 and l[0]) or\
            (len(set(l[1:])) == 1 and l[-1]):
            winner = l[0] or l[-1]
            pg.draw.line(screen, (250, 0, 0),
                         (0, (row + 1) * height / N - height / (N * 2)),
                         (width, (row + 1) * height / N - height / (N * 2)),
                         4)
            break

    # checking for winning columns
    for col in range(N):
        l = [board[i][col] for i in range(N)]
        if (len(set(l[:-1])) == 1 and l[0]) or \
            (len(set(l[1:])) == 1 and l[-1]):
            winner = l[0] or l[-1]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / N - width / (N * 2), 0), # replace N*2 with 6
                         ((col + 1) * width / N - width / (N * 2), height), 4)
            break

    # check for diagonal winners
    l = [board[i][i] for i in range(N)]
    if (len(set(l[:-1])) == 1 and l[0]) or \
        (len(set(l[1:])) == 1 and l[-1]):
        winner = l[0] or l[-1]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (450, 450), 4)

    l = [board[i+1][i] for i in range(4)]
    if (len(set(l)) == 1 and l[0]):
        winner = l[0]
        pg.draw.line(screen, (250, 70, 70), (50, 150), (350, 450), 4)

    l = [board[i][i+1] for i in range(4)]
    if (len(set(l)) == 1 and l[0]):
        winner = l[0]
        pg.draw.line(screen, (250, 70, 70), (150, 50), (450, 350), 4)

    l = [board[i][-i-1] for i in range(N)]
    if (len(set(l[:-1])) == 1 and l[0]) or \
        (len(set(l[1:])) == 1 and l[-1]):
        winner = l[0] or l[-1]
        pg.draw.line(screen, (250, 70, 70), (450, 50), (50, 450), 4)

    l = [board[i+1][-i-1] for i in range(4)]
    if (len(set(l)) == 1 and l[0]):
        winner = l[0]
        pg.draw.line(screen, (250, 70, 70), (450, 150), (150, 450), 4)

    l = [board[i][-i-2] for i in range(4)]
    if (len(set(l)) == 1 and l[0]):
        winner = l[0]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if all([all(row) for row in board]) and winner is None:
        draw = True
    draw_status()


def drawXO(row, col):
    global board, XO

    # for the first row, the image
    # should be pasted at a x coordinate
    # of 30 from the left margin
    posx = width / N * (row - 1) + 12000 // width
    posy = height / N * (col - 1) + 12000 // height

    # setting up the required board
    # value to display
    board[row - 1][col - 1] = "X" if XO else "O"
    if XO:
        # pasting x_img over the screen
        # at a coordinate position of
        # (pos_y, posx) defined in the
        # above code
        screen.blit(x_img, (posy, posx))
        XO ^= 1
    else:
        screen.blit(o_img, (posy, posx))
        XO ^= 1
    pg.display.update()


def user_click():
    # get coordinates of mouse click
    x, y = pg.mouse.get_pos()

    row, col = None, None
    # get column of mouse click (1-N)
    for i in range(N, 0, -1):
        if x < width / N * i:
            col = i

    # get row of mouse click (1-N)
    for i in range(N, 0, -1):
        if y < height / N * i:
            row = i

    # after getting the row and col,
    # we need to draw the images at
    # the desired positions
    if (row and col and board[row - 1][col - 1] is None):
        global XO
        drawXO(row, col)
        check_win()


def reset_game():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 1
    draw = False
    game_initiating_window()
    winner = None
    board = [[None] * N for _ in range(N)]


game_initiating_window()

while (True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            user_click()
            if (winner or draw):
                time.sleep(3)
                exit(0)
                # reset_game() # reset the game instead of quitting the window
    pg.display.update()
    CLOCK.tick(fps)