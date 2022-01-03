from numpy.core.shape_base import block
from Utils import is_safe, scan_one_square_visibility, is_available_move, heuristic_move, get_seeker_vision
import numpy as np
from Direction import directions, vision_direction
from random import randint
from math import pow
import copy as cp
class GameMap:
    def __init__(self, size):
        self.size = size
        self.hider = [0,0]
        self.seeker = []
        self.num_action = 5
        self.list_action = np.array(np.identity(self.num_action, dtype=int).tolist())
        self.lose = -300
        self.win = 150
        self.stuck = -1000
        self.fill_the_hole = 50
        self.hidden_rewards = [-20, -10, 5, 20, 30, 50, 70, 90, 110]
        self.seeker_target = [1, 4]
        self.seeker_vision = []
        self.initialize_map()
    def initialize_map(self):
        #create a custom map -> will change to read text file in the future

        self.map = np.zeros([self.size, self.size], dtype=int)
        self.add_hider(1,1)
        self.add_seeker(0,10)
        self.num_obstacles = 1
        self.num_state = int(pow(10,6))
        self.map[0][4] = 1
        self.map[1][2] = 2
        self.map[2][4] = 1
        self.map[3][4] = 1
        self.map[4][4] = 1
        self.map[2][3] = 2
        self.map[4][2] = 1
        self.map[2][1] = 2
        self.map[4][0] = 1
        self.hole_position = [[1,4], [4,3], [4,1]]
        self.num_holes_remained = 3
        self.num_holes = 3
        return 0

    def add_hider(self, x, y):
        self.hider = [x,y]
        self.map[x][y] = 3

    def add_seeker(self, x,y):
        self.seeker = [x,y]
        self.map[x][y] = 4

    def move_hider(self, hider, index):
        next_x = hider[0] + directions[index][0]
        next_y = hider[1] + directions[index][1]
        flag, is_available = is_available_move(self.map,next_x, next_y, self.size, directions[index])
        # nuoc di thanh cong -> return 0, else -1
        if not is_available:
           return [-1,-1,-1]
        self.map[hider[0]][hider[1]] = 0
        hider[0] += directions[index][0]
        hider[1] += directions[index][1]
        if flag == 1:    
            self.map[hider[0]+directions[index][0]][hider[1]+directions[index][1]] = 2 #dich chuyen vat can
        self.map[hider[0]][hider[1]] = 3
        return (flag,hider[0], hider[1])

    def step(self, counter, action, pregame=True):
        done = False
        reward = 0
        score = 0
        if pregame:
            flag, x, y = self.move_hider(self.hider, action)
            if flag == -1:
                reward += self.stuck
                done = True
            else:
                if flag ==1:
                    count = self.num_holes
                    for hole in self.hole_position:
                        if self.map[hole[0]][hole[1]] == 2:
                            count-=1
                    if count<self.num_holes_remained:
                        self.num_holes_remained = count
                        reward+=50
                    elif count>self.num_holes_remained:
                        print(count,self.num_holes_remained,"yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
                        self.num_holes_remained = count
                        reward-=150
                self.hider = [x,y]
        else:
            self.move_seeker(counter)
        
        if self.seeker[0] == self.hider[0] and self.seeker[1] == self.hider[1]:
            reward += self.lose
            done = True
        if counter == 0:
            done = True
            reward += self.win
        state = self.set_info(done)

        print('Reward: ', reward)
        print('Score: ', score)
        print('Done: ', done)
        print('State: ', state)
        # if not pregame:
        #     for i in range (len(self.seekers)):
        #         x,y = self.seekers[i]
        #         index = randint(0, 4)
        #         next_x = x + directions[index][0]
        #         next_y = y + directions[index][1]
        #         while not is_available_move(self.map,next_x, next_y, self.size, directions[index]):
        #             index = randint(0, 4)
        #             next_x = x + directions[index][0]
        #             next_y = y + directions[index][1] 
        return state, reward, done, score

    def reset(self):
        self.initialize_map()
        self.seeker_vision = []
        return self.set_info(done=False)

    def set_info(self, done=False):
        state = 0
        for i in range (self.size):
            for j in range (self.size):
                position = i*self.size+j
                if self.map[i][j] == 3:
                    state += position*1000
                elif self.map[i][j] == 4:
                    state += 0
                else:
                    state += position*self.map[i][j]
        return state

    def move_seeker(self, counter):
        if self.map[1][4] == 2:
            self.seeker_target = [4,1]
        if self.map[4][1] == 2:
            self.seeker_target = [4,3]
        a,b,seeker_vision  = get_seeker_vision(self.seeker, self.map, self.size) # a, b is the thief position if found
        self.seeker_vision = seeker_vision
        if a!= -1:
            self.seeker_target = [a,b]
        elif counter % 2 == 0:
            self.seeker_target = [self.hider[0] + randint(-2,2), self.hider[1] + randint(-2,2)]
        [x,y] = heuristic_move(self.map, self.seeker[0], self.seeker[1], self.seeker_target[0], self.seeker_target[1], self.size)
        self.map[self.seeker[0]][self.seeker[1]] = 0
        self.seeker = [x,y]
        self.map[x][y] = 4
    

