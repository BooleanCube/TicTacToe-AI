import numpy as np
import pygame as pg
import sys
import os
import time
from pygame.locals import *
from algorithms.neural_network import NeuralNetwork
from data.getter import get_data

# declaring the global variables
XO = 2 # 2 represents 'X' adn 3 represents 'O'
N = 5

# initialize the neural network and data
cpu = NeuralNetwork(N)
boards, labels = get_data(os.getcwd() + f"/data/ttt_dataset{N}x{N}.csv")


# train the neural network for 3 epochs
for epoch in range(1, 4):
    start = time.time()
    correct, total = 0, 0
    for state, label in zip(boards, labels):
        total += 1
        output = cpu.feed_forward(state)
        # print("here")
        # print(label, np.argmax(output))
        if np.argmax(output) == label: correct += 1
        cpu.back_propagate(label)

    print(f"Epoch #{epoch}:")
    print(f"Accuracy: {round(correct/total * 100, 2)}%")
    print(f"Epoch runtime: {time.time() - start} seconds")

winner = None
draw = None
width, height = 500, 500

white = (255, 255, 255)
line_color = (0, 0, 0)

board = [[None] * N for _ in range(N)]

pg.init()
fps = 30
CLOCK = pg.time.Clock()

screen = pg.display.set_mode((width, height + 100), 0, 32)

pg.display.set_caption("Tic Tac Toe")

# loading the images as python object
initiating_window = pg.image.load("assets/modified_cover.png")
x_img = pg.image.load("assets/X_modified.png")
y_img = pg.image.load("assets/o_modified.png")

# resizing images
initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (32000 // width, 32000 // height))
o_img = pg.transform.scale(y_img, (32000 // width, 32000 // height))


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
    global draw

    if winner is None: message = ("X" if XO == 2 else "O") + "'s Turn"
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

    posx = width / N * (row - 1) + 12000 // width
    posy = height / N * (col - 1) + 12000 // height

    board[row - 1][col - 1] = "X" if XO == 2 else "O"
    if XO == 2:
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
                # reset_game()  # reset the game instead of quitting the window
    pg.display.update()
    CLOCK.tick(fps)