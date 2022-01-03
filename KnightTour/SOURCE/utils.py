def is_safe(x,y,size,board):
    if x<0 or x>= size or y<0 or y>= size or board[x][y] != -1:
        return False
    return True

def print_solution(board):
    for i in range (0,board.shape[0]):
        s = ""
        for j in range (0,board.shape[0]):
            s += str(board[i][j]) + ' '
        print(s)

def is_closed_tour(ix, iy, x,y):
    if abs(ix-x)*abs(iy-y) == 2:
        return True
    return False
