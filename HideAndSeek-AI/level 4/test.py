import numpy as np
qtable = np.zeros([10, 5])
qtable[0][4] = 1
print(np.argmax(qtable[0,:]))