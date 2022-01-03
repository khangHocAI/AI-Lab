import pygame
import random
from queue import Queue
pygame.init()
random.seed(56)
height= 576#12
width= 624
num_square_onY=-1
num_square_onX=-1
width_each_square=48

#0 is empty, 1 is wall, 2 is thief, 3 is police
file_object= open('map1.txt','r')
l= [[int(num) for num in line.split(' ')]for line in file_object]
num_square_onX=l[0][0]
num_square_onY=l[0][1]
location= [[0 for i in range(num_square_onX)]for j in range(num_square_onY)]

for i in range(num_square_onY):
    for j in range(num_square_onX):
        location[i][j]= l[i+1][j]


screen= pygame.display.set_mode((width,height))
running= True
current_time=0

#title
pygame.display.set_caption("Hide and seek with idiot AI agent")
icon = pygame.image.load('death.png')
pygame.display.set_icon(icon)
def convertLocationOnMatrix_ToOnConsole(x):
    return (x*48)+8


class Wall:
    def __init__(self,X,Y):
        self.X_onMatrix=X
        self.Y_onMatrix=Y
        # tempX = random.randrange(0, num_square_onX, 1)
        # tempY = random.randrange(0, num_square_onY, 1)
        # while location[tempY][tempX] != 0:# occupy
        #     tempX = random.randrange(0, num_square_onX, 1)
        #     tempY = random.randrange(0, num_square_onY, 1)
        # location[tempY][tempX]=3
        # self.X_onMatrix=tempX
        # self.Y_onMatrix= tempY
    def setXMatrix(self,_X):
        self.X_onMatrix=_X
    def setYMatrix(self,_Y):
        self.Y_onMatrix=_Y
    def getXMatrix(self):
        return self.X_onMatrix
    def getYMatrix(self):
        return self.Y_onMatrix
    def put(self,img):
        screen.blit(img, (convertLocationOnMatrix_ToOnConsole(self.X_onMatrix),convertLocationOnMatrix_ToOnConsole(self.Y_onMatrix)))


class Police:
    def __init__(self,_R,X,Y):#v is veclocity, R is radius of view
        self.X_onMatrix = X
        self.Y_onMatrix = Y
        self.prev_X=-1
        self.prev_Y=-1
        # tempX = random.randrange(0, num_square_onX, 1)
        # tempY = random.randrange(0, num_square_onY, 1)
        # while location[tempY][tempX] != 0:  # occupy
        #     tempX = random.randrange(0, num_square_onX, 1)
        #     tempY = random.randrange(0, num_square_onY, 1)
        # location[tempY][tempX] = 1
        # self.X_onMatrix = tempX
        # self.Y_onMatrix = tempY
        self.R= _R
        self.moveX = [1, 0, -1, 1, -1, 0,  -1, 1]
        self.moveY = [0, 1, -1, 1, 0, -1,  1, -1]
        self.targetLocation=[]
    def getTargetContainer(self):
        return self.targetLocation
    def addTargetLocation(self,loca):
        self.targetLocation.append(loca)
    def setXMatrix(self,_X):
        self.X_onMatrix=_X
    def setYMatrix(self,_Y):
        self.Y_onMatrix=_Y
    def getXMatrix(self):
        return self.X_onMatrix
    def getYMatrix(self):
        return self.Y_onMatrix
    def getPreviousMoveX(self):
        return self.prev_X
    def getPreviousMoveY(self):
        return self.prev_Y
    def clearTarget(self):
        for i in range(len(self.targetLocation)):
            # print(self.targetLocation[j][0],self.targetLocation[j][1])
            print('X',self.targetLocation[i][1])
            print('Y',self.targetLocation[i][0])

            if location[self.targetLocation[i][1]][self.targetLocation[i][0]] != 2:
                self.targetLocation.pop(i)

    def changeLocation(self):
        #self.clearTarget()
        # for i in location:
        #     print(i)
        #print(len(self.targetLocation))
        #print(self.targetLocation)
        if len(self.targetLocation)==0:#not find anything
            idx = random.randrange(0, 8, 1)
            n_x = self.X_onMatrix + self.moveX[idx]
            n_y = self.Y_onMatrix + self.moveY[idx]
            while not self.isSafe(n_x, n_y):
                idx = random.randrange(0, 8, 1)
                n_x = self.X_onMatrix + self.moveX[idx]
                n_y = self.Y_onMatrix + self.moveY[idx]
            location[self.Y_onMatrix][self.X_onMatrix] = 0
            self.prev_X= self.X_onMatrix
            self.prev_Y= self.Y_onMatrix
            self.X_onMatrix = n_x
            self.Y_onMatrix = n_y
            #print('n',n_x,n_y)
            #print(self.X_onMatrix,self.Y_onMatrix)
            #print(location)
            location[self.Y_onMatrix][self.X_onMatrix] = 3
        else:
            move_idx = -1
            min_dis = 1000
            tempList = []
            for i in range(len(self.targetLocation)):
                #print(self.targetLocation[j][0],self.targetLocation[j][1])
                if location[self.targetLocation[i][1]][self.targetLocation[i][0]]==2:
                    tempList.append([self.targetLocation[i][0],self.targetLocation[i][1]])
            self.targetLocation= tempList
            for j in range(len(self.targetLocation)):
                for i in range(8):
                    next_x = self.X_onMatrix + self.moveX[i]
                    next_y = self.Y_onMatrix + self.moveY[i]
                    dis = abs(self.targetLocation[j][0] - next_x) + abs(self.targetLocation[j][1] - next_y)
                    if self.isSafe(next_x,next_y) and  dis < min_dis:
                        min_dis = dis
                        move_idx = i

            if self.prev_X== self.X_onMatrix+self.moveX[move_idx] and self.prev_Y== self.Y_onMatrix+self.moveY[move_idx]:
                # overlap move, random move
                idx = random.randrange(0, 8, 1)
                n_x = self.X_onMatrix + self.moveX[idx]
                n_y = self.Y_onMatrix + self.moveY[idx]
                while not self.isSafe(n_x, n_y):
                    idx = random.randrange(0, 8, 1)
                    n_x = self.X_onMatrix + self.moveX[idx]
                    n_y = self.Y_onMatrix + self.moveY[idx]
                location[self.Y_onMatrix][self.X_onMatrix] = 0
                self.prev_X = self.X_onMatrix
                self.prev_Y = self.Y_onMatrix
                self.X_onMatrix = n_x
                self.Y_onMatrix = n_y
                # print('n',n_x,n_y)
                # print(self.X_onMatrix,self.Y_onMatrix)
                # print(location)
                location[self.Y_onMatrix][self.X_onMatrix] = 3
            else:
                location[self.Y_onMatrix][self.X_onMatrix] = 0
                self.prev_X = self.X_onMatrix
                self.prev_Y = self.Y_onMatrix
                self.X_onMatrix = self.X_onMatrix + self.moveX[move_idx]
                self.Y_onMatrix = self.Y_onMatrix + self.moveY[move_idx]
                location[self.Y_onMatrix][self.X_onMatrix] = 3
            #print(location)

    def markTheView(self):
        for i in range(8):
            n_x= self.X_onMatrix
            n_y= self.Y_onMatrix
            #print(location[n_y][n_x])
            for j in range(self.R):
                n_x = n_x + self.moveX[i]
                n_y = n_y + self.moveY[i]
                if n_x>=0 and n_x<num_square_onX and n_y>=0 and n_y < num_square_onY and location[n_y][n_x]!=1:#not trap
                    if location[n_y][n_x]==2:#find the thief
                        self.addTargetLocation([n_x,n_y])
                    elif location[n_y][n_x]==0:
                        X_map= convertLocationOnMatrix_ToOnConsole(n_x)
                        Y_map= convertLocationOnMatrix_ToOnConsole(n_y)
                        pygame.draw.circle(screen, (209, 41, 41), (X_map + 17 , Y_map +17), self.R * 5)
                else:
                    break
    def put(self,img,flag):
        if flag:
            self.changeLocation()
            self.markTheView()
        # else:
        #     self.markTheView()
        screen.blit(img, (convertLocationOnMatrix_ToOnConsole(self.X_onMatrix), convertLocationOnMatrix_ToOnConsole(self.Y_onMatrix)))
    def isSafe(self,x,y):
        return (x>=0 and x<num_square_onX and y>=0 and y< num_square_onY and location[y][x]!=1)#not ob

class Robber:
    def __init__(self,_R,X,Y):
        self.X_onMatrix = X
        self.Y_onMatrix = Y
        self.R= _R
        self.moveX = [1, 0, -1, 1, -1, 0, -1, 1]
        self.moveY = [0, 1, -1, 1, 0, -1, 1, -1]
        self.isFindPolice=False
        self.isCatch=False
    def Catch(self):
        return self.isCatch
    def setPoliceX(self,X):
        self.policeX=X
    def setPoliceY(self,Y):
        self.policeY=Y
    def setXMatrix(self,_X):
        self.X_onMatrix=_X
    def setYMatrix(self,_Y):
        self.Y_onMatrix=_Y
    def getXMatrix(self):
        return self.X_onMatrix
    def getYMatrix(self):
        return self.Y_onMatrix
    # def setCatch(self):
    #     self.isCatch = True
    def changeLocation(self):
        if not self.isFindPolice:  # not find anything
            idx = random.randrange(0, 8, 1)
            n_x = self.X_onMatrix + self.moveX[idx]
            n_y = self.Y_onMatrix + self.moveY[idx]
            while not self.isSafe(n_x, n_y):
                idx = random.randrange(0, 8, 1)
                n_x = self.X_onMatrix + self.moveX[idx]
                n_y = self.Y_onMatrix + self.moveY[idx]
            location[self.Y_onMatrix][self.X_onMatrix] = 0
            self.X_onMatrix = n_x
            self.Y_onMatrix = n_y
            location[self.Y_onMatrix][self.X_onMatrix] = 2
        else:
            move_idx = -1
            max_dis = -1
            #tempList = []
            # for i in range(len(self.targetLocation)):
            #     if location[self.targetLocation[i][1]][self.targetLocation[i][0]] == 1:
            #         tempList.append([self.targetLocation[i][0], self.targetLocation[i][1]])
            #self.targetLocation = tempList
            for i in range(8):
                next_x = self.X_onMatrix + self.moveX[i]
                next_y = self.Y_onMatrix + self.moveY[i]
                dis = abs(self.targetLocation[j][0] - next_x) + abs(self.targetLocation[j][1] - next_y)
                if self.isSafe(next_x, next_y) and dis > max_dis:
                    max_dis = dis
                    move_idx = i
            location[self.Y_onMatrix][self.X_onMatrix] = 0
            self.X_onMatrix = self.X_onMatrix + self.moveX[move_idx]
            self.Y_onMatrix = self.Y_onMatrix + self.moveY[move_idx]
            location[self.Y_onMatrix][self.X_onMatrix] = 2
    def checkIsCatch(self,policeX,policeY):
        if self.X_onMatrix== policeX and self.Y_onMatrix == policeY:
            self.isCatch= True
            location[self.Y_onMatrix][self.X_onMatrix] = 0
            return True
        return False

    def markTheView(self):
        for i in range(8):
            n_x = self.X_onMatrix
            n_y = self.Y_onMatrix
            #print(location[n_y][n_x])
            for j in range(self.R):
                n_x = n_x + self.moveX[i]
                n_y = n_y + self.moveY[i]
                if n_x >= 0 and n_x < num_square_onX and n_y >= 0 and n_y < num_square_onY and location[n_y][n_x] != 3:  # not trap
                    if location[n_y][n_x] == 3:  # find the thief
                        self.isFindPolice=True
                        self.setPoliceX(n_x)
                        self.setPoliceY(n_y)
                    elif location[n_y][n_x] == 0:
                        X_map = convertLocationOnMatrix_ToOnConsole(n_x)
                        Y_map = convertLocationOnMatrix_ToOnConsole(n_y)
                        pygame.draw.circle(screen, (253, 237, 17), (X_map + 17, Y_map + 17), self.R * 3)
                else:
                    break
    def put(self, img, flag):
        if not self.isCatch:
            if flag:
                self.changeLocation()
                self.markTheView()
            # else:
            #     self.markTheView()
            screen.blit(img, (convertLocationOnMatrix_ToOnConsole(self.X_onMatrix), convertLocationOnMatrix_ToOnConsole(self.Y_onMatrix)))
    def isSafe(self, x, y):
        return (x >= 0 and x < num_square_onX and y >= 0 and y < num_square_onY and location[y][x] == 0)  # not ob and not police

#police

policeImg= pygame.image.load('policecar32.png')
robberImg= pygame.image.load('hacker32.png')
wallImg= pygame.image.load('tree.png')
background= pygame.image.load('background.PNG')
def drawBackGround():
    screen.blit(background, (0, 0))
#policeX,policeY=0,0

# num_robber=0
# num_wall=0
# num_police= 0
police=None
robber= []
wall=[]
#0 is empty, 1 is wall, 2 is thief, 3 is police
for i in range(num_square_onY):
    for j in range(num_square_onX):
        location[i][j]= l[i+1][j]
        if location[i][j]==1:
            wall.append(Wall(j,i))
        elif location[i][j]==2:
            robber.append(Robber(2,j,i))
        elif location[i][j]==3:
            police=Police(3,j,i)

for i in range(len(wall)):
    wall[i].put(wallImg)
for i in range(len(robber)):
    robber[i].put(robberImg,False)#false is not run
police.put(policeImg,False)

drawBackGround()

pygame.display.update()

cnt=0
idxRobber=0
while running:
    drawBackGround()

    #screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#when press button exit
            running=False

    if cnt % 5 == 0:
        for i in range(len(robber)):
            if not robber[i].Catch():#is thief
                police.addTargetLocation([robber[i].getXMatrix(),robber[i].getYMatrix()])
    print(police.getTargetContainer())
    #print(police.getXMatrix())

    #print(police.getYMatrix())
    nb_robber_no_caught = 0
    police.put(policeImg,True)
    for i in range(len(robber)):
        if not robber[i].Catch():#not catch
            nb_robber_no_caught+=1
            res= robber[i].checkIsCatch(police.getXMatrix(),police.getYMatrix())
            if not res:#not catch
                if i==idxRobber:
                    robber[i].put(robberImg,True)
                else:
                    robber[i].put(robberImg,False)

    if nb_robber_no_caught==0:
        break

    for i in range(len(wall)):
        wall[i].put(wallImg)




    num_robber= len(robber)
    idxRobber+=1
    if idxRobber==num_robber:
        idxRobber=0

    pygame.display.update()
    pygame.time.delay(500)
    cnt+=1
    if cnt==100:#test case
        running=False

