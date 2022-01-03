import utils as ut
from random import randint
import sys
import numpy as np
import time
def get_degree(x,y, possible_moves, board, size):
    degree = 0
    for i in range(8):
	    if ut.is_safe(x+possible_moves[i][0],y+possible_moves[i][1],size,board):
		    degree += 1
    return degree

def next_move(board, position, possible_moves, size):
    min_deg_idx = -1
    min_deg = 8
    x = position[0]
    y = position[1]
    start = randint(0,8)
    for i in range (0, 8):
        index = (start + i)%8
        next_x = x + possible_moves[index][0]
        next_y = y + possible_moves[index][1]
        degree = get_degree(next_x, next_y, possible_moves, board, size)
        if ut.is_safe(next_x, next_y, size, board) and degree<min_deg:
            min_deg_idx = i; 
            min_deg = degree
            position[0] = next_x
            position[1] = next_y
    if min_deg_idx == -1:
        return False
    return True

def warnsdoff(x, y, possible_moves, board, size):
    move = [x,y]
    for i in range (0, size*size-1):
        if next_move(board, move, possible_moves, size) == False:
            return False
        board[move[0]][move[1]] = i + 2
    if ut.is_closed_tour(x,y, move[0], move[1]) == False:
        time.sleep(3)
        return False
    return True

argument_list = sys.argv[1:]
input = argument_list[1::2]
input = list(map(int, input))
px = input[0]
py = input[1]
s = input[2]
#Initialize the game:
board = np.ones([s,s]) * (-1)
board = board.astype(int)
board[px][py] = 1
possible_moves=[[2,1],[2,-1],[1,2],[1,-2],[-1,2],[-1,-2],[-2,1],[-2,-1]]
if s % 2 == 1:
    start_time = time.time()
    result = warnsdoff(px, py, possible_moves, board, s)
    print("Open tour:")
    print("--- Time run (ms) ---", (time.time() - start_time)*1000)
    ut.print_solution(board)
else:
    count = 1
    total_time = 0
    start_time = time.time()
    while(warnsdoff(px, py, possible_moves, board, s) == False and count < 100):
        print("Open tour:", count)
        running_time = (time.time() - start_time)*1000
        total_time += running_time
        print("--- Time run (ms)---", running_time)
        if count == 1:
            ut.print_solution(board)
        start_time = time.time()
        board = np.ones([s,s]) * (-1)
        board = board.astype(int)
        board[px][py] = 1
        count+=1

    if count == 100:
        print("Can't find closed tour at this position.")    
    else:
        print("find solution after ", count, " runs")
        print("--- Time run (ms)---", total_time)
        ut.print_solution(board)
