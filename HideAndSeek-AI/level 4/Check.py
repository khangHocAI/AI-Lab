import numpy as np
from GameMap import GameMap
def check(ave, q):
    game_map = GameMap(12)
    game_map.reset()
    qtable = q
    list_score = []
    total_reward = []

    for _ in range(ave):
        state = game_map.reset()
        # evn2.view()
        score = 0
        rewards = 0
        done = False
        index = 0
        counter = 4
        while counter > 0:
            # time.sleep(0.5)
            action = np.argmax(qtable[state, :])
            print(action)
            new_state, reward, done, info = game_map.step(counter, action, pregame=True)
            # evn2.view()
            rewards += reward
            score = info
            if done:
                break
            state = new_state
            index+=1
            if index == 10:
                index = 0
                counter-=1
        counter = 8
        index = 0
        while counter > 0:
            action = np.argmax(qtable[state, :])
            print(action)
            new_state, reward, done, info = game_map.step(counter, action, pregame=False)
            # evn2.view()
            rewards += reward
            score = info
            if done:
                break
            state = new_state
            index+=1
            if index == 10:
                index = 0
                counter-=1
        list_score.append(score)
        total_reward.append(rewards)
    print('Max dot: ', max(list_score), ' Min dot: ', min(list_score))
    return sum(list_score)/ave, sum(total_reward)/ave