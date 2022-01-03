import pygame
from Direction import vision_direction

def is_safe(x, y, size):
    if x<0 or y<0 or y>=size or x >= size:
        return False
    return True

def is_empty(map,x,y,size):
    if is_safe(x,y,size) and map[x][y] == 0:
        return True
    return False
def is_seeker_visible(map, x, y, size):
    if is_safe(x,y,size) and (map[x][y] == 0 or map[x][y] == 3):
        return True
    return False
def scan_one_square_visibility(map, size, x, y):
    
    vision = 0
    for i in range (8):
        next_x = vision_direction[i][0] + x
        next_y = vision_direction[i][1] + y
        if is_empty(map, next_x,next_y, size):
            vision+=1
            # if map[next_x][next_y] == 0:
                # vision.append([next_x, next_y])
                # available_move.append([next_x, next_y])
            # elif map[next_x][next_y] == 2 and is_empty(map,next_x+move[i][0],next_y+move[i][1],size):
                # available_move.append([next_x, next_y])
    return vision

def is_available_move(map, x,y,size,direction):
    if is_empty(map, x,y, size):
        return (0,True)
    if is_safe(x,y,size) and is_empty(map,x+direction[0], y+direction[1],size) and map[x][y] ==2:
        return (1,True)
    return (-1,False)

def heuristic_move(map, x,y, target_x, target_y,size):
    next_x = 0
    next_y = 0
    move = [[0,1], [1,0], [0, -1], [-1, 0],[1,-1], [-1,-1], [1,1],[-1,1]]
    move_idx = -1
    min_dis = 100
    for i in range (8):
        next_x = x + move[i][0]
        next_y = y + move[i][1]
        dis = abs(target_x - next_x) + abs(target_y - next_y)
        if is_seeker_visible(map, next_x, next_y, size) and dis < min_dis:
            min_dis = dis
            move_idx = i
    next_x = x + move[move_idx][0]
    next_y = y + move[move_idx][1]
    return [next_x,next_y]

def draw_one_square_vision(screen, x, y, flag=0):
    if flag == 0:
        pygame.draw.rect(screen, (255,0,0),(y*45+10,x*45+10,40,40))
    else:
        pygame.draw.rect(screen, (0,0,255),(y*45+10,x*45+10,40,40))

def draw_vision(screen, map, seeker_vision, flag=0):
    for vision in seeker_vision:
        for square in vision:
            draw_one_square_vision(screen, square[0], square[1])
def seeker_scanning_around(map,seeker, size, direction):
    hider_position = [-1,-1]
    list_vision = []
    for i in range (1,3):
        x = seeker[0]+direction[0]*i
        y = seeker[1]+direction[1]*i
        if is_seeker_visible(map, x, y, size):
            list_vision.append([x,y])
            if map[x][y] == 3:
                hider_position = [x,y]
        else:
            break
    return hider_position[0], hider_position[1], list_vision

def get_seeker_vision(seeker, map, size):
    hider_position = [-1,-1]
    seeker_vision = []
    for direction in vision_direction:
        a,b,vision  = seeker_scanning_around(map, seeker, size, direction)
        seeker_vision.append(vision)
        if a != -1:
            hider_position = [a,b]
    return hider_position[0], hider_position[1], seeker_vision

