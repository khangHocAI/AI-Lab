from Utils import draw_vision
from GameMap import GameMap
from Hider import Hider
from Seeker import Seeker
from DrawMap import draw_map
import pygame
import numpy as np
import config
import matplotlib.pyplot as plt
import random as rd
from Check import check
pygame.init()
pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
pygame.display.set_caption("Level 4")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pre_game_counter, pre_game_text = 4, '4'.rjust(3)
counter, text = 8, '8'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
seeker_image = pygame.image.load('policeman.png') 
hider_image = pygame.image.load('thief.png') 

game_map = GameMap(12)
#########################################
Init = config.INIT_Q_Learning
action_size = len(game_map.list_action)
state_action = int(game_map.num_state)
qtable = np.zeros([state_action, action_size])
if Init == False:
    Best_Q = np.load('Best-Q.npy')
    max_ave = Best_Q[0][0]
    best_q = Best_Q[1]
    # print(max_ave)
    # print(best_q)
else:
    max_ave = 0

total_episodes = config.total_episodes
learning_rate = config.learning_rate
max_step = game_map.size * game_map.size
gamme = config.gamme
episodes_check = config.episodes_check

epsilon = config.epsilon
max_epsilon = config.max_epsilon
min_epsilon = config.min_epsilon
decay_rate = config.decay_rate
#####################################################################
######################################################################
######################################################################33
tranning = True
running = True
if tranning:
    if Init == False:
        info = np.load('Q-Table.npy')
        qtable = info[1]
        episodest = info[0][0]
        epsilon = info[0][1]
        # print(qtable)
    else:
        episodest = 0
        np.save('Q-Table', np.array([[0, epsilon], qtable]))

    episodes = []
    rewards = []
    scores = []

    for i in range(total_episodes):
        episode = episodest+i
        state = game_map.reset()
        done = False
        total_rewards = 0
        score = 0
        pre_game_counter = 4
        counter = 8
        running = True
        pregame = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    if pregame: 
                        pre_game_counter -= 1
                        pre_game_text = str(pre_game_counter).rjust(3) if pre_game_counter > 0 else 'Game start!'
                        if pre_game_counter == 0: 
                            pre_game_counter = 8
                            print("ok")
                            pregame = False
                    else:
                        pre_game_counter -= 1
                        pre_game_text = str(pre_game_counter).rjust(3) if pre_game_counter > 0 else 'Game over!'
                        if pre_game_counter == 0: 
                            running = False
            exp = rd.uniform(0, 1)
            if exp > epsilon:
                action = np.argmax(qtable[state, :])
            else:
                same = np.where(qtable[state, :] == np.max(qtable[state, :]))
                action = rd.choice(same[0])
            new_state, reward, done, info = game_map.step(pre_game_counter, action, pregame)
            score = info
            qtable[state, action] = qtable[state, action]+learning_rate*(reward+gamme*np.max(qtable[new_state, :]) - qtable[state, action])
            print(qtable[state, action])
            total_rewards += reward
            state = new_state
            screen.fill((255,255,255))
            draw_map(screen, game_map.size, game_map.map, hider_image,seeker_image)
            draw_vision(screen, game_map.map, game_map.seeker_vision)
            screen.blit(myfont.render(pre_game_text, True, (0, 0, 0)), (600, 48))
            clock.tick(60)
            pygame.time.wait(100)
            pygame.display.update()
            if done:
                running = False
            print('Episode {}: rate: {} - hidden score: {} - rewards: {}'.format(episode, epsilon, score, total_rewards))
            if (episode+1) % episodes_check == 0 or episode == 0:
                np.save('Q-Table', np.array([[episode+1, epsilon], qtable]))
            # print('Saved Qtable')
                tscore, treward = check(3, qtable)
            # print('Ave D= ', tscore)
                if treward > max_ave:
                    max_ave = treward
                    np.save('Best-Q', np.array([[max_ave], qtable]))

                if Init == False:
                    episodes = np.load('E-Q.npy')
                    episodes = np.hstack((episodes, np.array([episode])))
                    scores = np.load('S-Q.npy')
                    scores = np.hstack((scores, np.array([tscore])))
                    rewards = np.load('R-Q.npy')
                    rewards = np.hstack((rewards, np.array([treward])))

                    np.save('E-Q', np.array(episodes))
                    np.save('S-Q', np.array(scores))
                    np.save('R-Q', np.array(rewards))
                else:
                    np.save('E-Q', np.array([]))
                    np.save('S-Q', np.array([]))
                    np.save('R-Q', np.array([]))
                    break

            epsilon = min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*episode)

        print(qtable)

else:
    done = False
    total_rewards = 0
    score = 0
    pre_game_counter = 20
    running = True
    pregame = True
    state = game_map.reset()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if pregame: 
                    pre_game_counter -= 1
                    pre_game_text = str(pre_game_counter).rjust(3) if pre_game_counter > 0 else 'Game start!'
                    if pre_game_counter == 0: 
                        pre_game_counter = 40
                        print("ok")
                        pregame = False
                else:
                    pre_game_counter -= 1
                    pre_game_text = str(pre_game_counter).rjust(3) if pre_game_counter > 0 else 'Game over!'
                    if pre_game_counter == 0: 
                        running = False
        action = np.argmax(qtable[state, :])
        new_state, reward, done, info = game_map.step(pre_game_counter, action, pregame)
        state = new_state
        screen.fill((255,255,255))
        draw_map(screen, game_map.size, game_map.map, hider_image,seeker_image)
        draw_vision(screen, game_map.map, game_map.seeker_vision)
        screen.blit(myfont.render(pre_game_text, True, (0, 0, 0)), (600, 48))
        clock.tick(60)
        pygame.time.wait(500)
        pygame.display.update()
        if done:
            running = False


# running = True
# list_move = {}
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.USEREVENT: 
#             counter -= 1
#             text = str(counter).rjust(3) if counter > 0 else 'Time up!'
#             if counter == 0:
#                 running = False
#         if event.type == pygame.QUIT:
#             running = False
#     screen.fill((255,255,255))
#     game_map.step(counter,pregame=False)
#     draw_map(screen, game_map.size, game_map.map, hider_image,seeker_image)
#     screen.blit(myfont.render(text, True, (0, 0, 0)), (600, 48))
#     clock.tick(60)
#     pygame.time.wait(500)
#     pygame.display.update()
# pygame.time.wait(3000)