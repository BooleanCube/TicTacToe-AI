import csv
import os

N = 5


def get_data(path):
    boards, labels = [], []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        f = 1
        for line in reader:
            if f:
                f = 0
                continue
            board = list(map(int, line))
            label = board.pop(-1)
            boards.append(board)
            labels.append(label)
    return boards, labels
