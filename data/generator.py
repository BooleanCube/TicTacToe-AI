import csv
import os
import random
import time

N = 5

fields = [chr(i)+str(j) for i in range(ord('a'), ord('a')+5) for j in range(1, N+1)] + ["label"]
filename = os.getcwd() + f"/ttt_dataset{N}x{N}.csv"

data = []
board = [[None]*5 for _ in range(5)]


# 2 if X wins, 3 if O wins, -1 for a draw and -2 for undecided
# roughly ~300 operations
def check_win():
    global board

    # checking for winning rows
    for row in range(0, N):
        l = board[row]
        if (len(set(l[:-1])) == 1 and l[0]) or \
                (len(set(l[1:])) == 1 and l[-1]):
            return l[0] or l[-1]

    # checking for winning columns
    for col in range(N):
        l = [board[i][col] for i in range(N)]
        if (len(set(l[:-1])) == 1 and l[0]) or \
                (len(set(l[1:])) == 1 and l[-1]):
            return l[0] or l[-1]

    # check for diagonal winners
    l = [board[i][i] for i in range(N)]
    if (len(set(l[:-1])) == 1 and l[0]) or \
            (len(set(l[1:])) == 1 and l[-1]):
        return l[0] or l[-1]

    l = [board[i + 1][i] for i in range(4)]
    if len(set(l)) == 1 and l[0]:
        return l[0]

    l = [board[i][i + 1] for i in range(4)]
    if len(set(l)) == 1 and l[0]:
        return l[0]

    l = [board[i][-i - 1] for i in range(N)]
    if (len(set(l[:-1])) == 1 and l[0]) or \
            (len(set(l[1:])) == 1 and l[-1]):
        return l[0] or l[-1]

    l = [board[i + 1][-i - 1] for i in range(4)]
    if len(set(l)) == 1 and l[0]:
        return l[0]

    l = [board[i][-i - 2] for i in range(4)]
    if len(set(l)) == 1 and l[0]:
        return l[0]

    if all([all(row) for row in board]):
        return -1

    return -2


# roughly ~15000 operations
def almost_win():
    global board

    for i in range(N):
        for j in range(N):
            if board[i][j] is not None: continue
            board[i][j] = 3
            if check_win() == 3:
                board[i][j] = None
                return i, j, 3
            board[i][j] = 2
            if check_win() == 2:
                board[i][j] = None
                return i, j, 2
            board[i][j] = None

    return -1, -1, -1


# 2 if X is about to draw a force, 3 if O is about to draw a force, otherwise -1
def check_force():
    global board

    # checking for forcing rows
    for row in range(0, N):
        l = board[row]
        if l == [None, 2, 2, 2, None] or l == [None, 3, 3, 3, None]:
            return l[1]

    # checking for forcing columns
    for col in range(N):
        l = [board[i][col] for i in range(N)]
        if l == [None, 2, 2, 2, None] or l == [None, 3, 3, 3, None]:
            return l[1]

    # check for diagonal forcers
    l = [board[i][i] for i in range(N)]
    if l == [None, 2, 2, 2, None] or l == [None, 3, 3, 3, None]:
        return l[1]

    l = [board[i][-i - 1] for i in range(N)]
    if l == [None, 2, 2, 2, None] or l == [None, 3, 3, 3, None]:
        return l[1]

    return -1


def almost_force():
    global board

    for i in range(N):
        for j in range(N):
            if board[i][j] is not None: continue
            board[i][j] = 3
            if check_force() == 3:
                board[i][j] = None
                return i, j, 3
            board[i][j] = 2
            if check_force() == 2:
                board[i][j] = None
                return i, j, 2
            board[i][j] = None

    return -1, -1, -1


start_time = time.time()
XO = 3
move_stack = []
open_moves = set([(i, j) for i in range(N) for j in range(N)])
for _ in range(int(1e5)):
    op = random.random()
    if op >= 0.6 and move_stack or len(move_stack) == 25:
        x, y = move_stack.pop(-1)
        open_moves.add((x, y))
        board[x][y] = None
    else:
        x, y = random.choice(list(open_moves))
        open_moves.remove((x, y))
        move_stack.append((x, y))
        board[x][y] = (XO := XO ^ 1)

    # skip if not AI's turn
    if XO == 3: continue

    # one move away from win or loss (attack and defend strats)
    tx, ty, tt = almost_win()
    if tt > -1:
        flat = [0 if board[i][j] is None else board[i][j] for i in range(N) for j in range(N)]  # board state
        flat += [tx * N + ty]  # label
        data.append(flat)
        for _ in range(min(len(move_stack), 3)):
            x, y = move_stack.pop(-1)
            open_moves.add((x, y))
            board[x][y] = None
    # two moves away from win or loss (1 move away from force attack or defend)
    tx, ty, tt = almost_force()
    if tt > -1:
        flat = [0 if board[i][j] is None else board[i][j] for i in range(N) for j in range(N)]  # board state
        flat += [tx * N + ty]  # label
        data.append(flat)
        # TODO remove last move in stack


random.shuffle(data)

print(f"Writing {len(data)} cases to the dataset..")

with open(filename, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    writer.writerows(data)
    print(f"Done in {time.time() - start_time} seconds!")

# n moves away from winning (1 - 5)
# n moves away from losing (1 - 2) to defend against losses
# invalid moves should be punished (set activation values to 0)
# only 1 valid move remaining (for all 25 squares) (done)
#