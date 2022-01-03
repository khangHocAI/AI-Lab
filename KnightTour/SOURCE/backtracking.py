import utils as ut
import sys
import numpy as np
import time
from random import randint

def backtracking(board, possible_moves, x,y, current_move, size, ix,iy):
    if current_move == size * size +1:
        return True
    for i in range (0,8):
        next_x = x + possible_moves[i][0]
        next_y = y + possible_moves[i][1]
        if ut.is_safe(next_x, next_y, size,board):
            board[next_x][next_y] = current_move
            if backtracking(board, possible_moves, next_x,next_y, current_move+1, size, ix,iy):
                return True
            else:
                board[next_x][next_y] = -1
    return False


#Input parse
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
if s >=8: 
    print("Backtracking can't find solution for board >=8")
else:
    start_time = time.time()
    if backtracking(board, possible_moves, px,py, 2, s, px, py):
        print("Open knight tour solution:")
        print("---Time run (ms)---", (time.time() - start_time)*1000)
        ut.print_solution(board)
    else:
        print("No solution")    