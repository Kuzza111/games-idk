import pygame
import random
import math


class Cell:
    def __init__(self, cords):
        self.cords = cords
        self.rotation = [1, 0]
        self.lifeTime = 100
        self.isAlife = True
        
        
        
        self.genome = [None for _ in range(8)]       
        #self.speed = speed # или max speed и speed выбирается отдельно
        #self.findRadius = None

    def moveForward(self):
        #сделать проверку на возможность шага
            #клетка занята
                #клетки между начальной и конечной заняты

        # сделать шаг, заменить на ЗАПРОС шага, если можно - шаг
        self.cords[0]+=self.rotation[0]
        self.cords[1]+=self.rotation[1]

        # если за границей - переместиться, добавить проверку занята ли
        if self.cords[0]<0:self.cords[0]=screen.get_width()+self.cords[0]
        if self.cords[0]>screen.get_width():self.cords[0]=self.cords[0]-screen.get_width()

        if self.cords[1]<0:self.cords[1]=screen.get_height()+self.cords[1]
        if self.cords[1]>screen.get_height():self.cords[1]=self.cords[1]-screen.get_height()

    def turnRight(self):
        if self.rotation==[1,0]:self.rotation=[0,1]
        elif self.rotation==[0,1]: self.rotation=[-1,0]
        elif self.rotation==[-1,0]: self.rotation=[0,-1]
        elif self.rotation==[0,-1]: self.rotation=[1,0]

    def turnLeft(self):
        if self.rotation==[1,0]:self.rotation=[0,-1]
        elif self.rotation==[0,-1]: self.rotation=[-1,0]
        elif self.rotation==[-1,0]: self.rotation=[0,1]
        elif self.rotation==[0,1]: self.rotation=[1,0]

    def replicate(self):
        newCell = Cell([self.cords[0], self.cords[1]])
        newCell.rotation = self.rotation

#        newGenome = self.genome
#        for i in range(len(newGenome)):
#            if random.randint(0,99)>97:
#                newGenome[i]+=random.randint(-10,10)
#            if newGenome[i]>63:newGenome[i]-63
#            elif newGenome[i]<0:newGenome[i]+63
#        newCell.genome = newGenome

        alotCells.append(newCell)

    def die(self):
        self.isAlife = False

    def generateGenome(self): 
        for i in range(len(self.genome)):
            self.genome[i] = random.randint(0,63)





pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
running = True
dt = 0


alotCells = [Cell(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))) for _ in range(5)]
player = Cell([screen.get_width()/2, screen.get_height()/2])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")


    # ai cells ######################################################
    for i in range(len(alotCells)):
        alotCells[i].moveForward()
        if random.randint(0, 99)>95:
            if random.randint(0, 1)==0: alotCells[i].turnLeft()
            else: alotCells[i].turnRight()
        if random.randint(0, 99)>97:
            if len(alotCells) < 500:
                alotCells[i].replicate()
        alotCells[i].lifeTime-=1
        if alotCells[i].lifeTime==0: alotCells[i].die()
        if alotCells[i].isAlife: pygame.draw.rect(screen, "red", (alotCells[i].cords[0], alotCells[i].cords[1], 3, 3))

    alifeCells = []
    for i in range(len(alotCells)):
        if alotCells[i].isAlife: alifeCells.append(alotCells[i])
    alotCells = alifeCells
    
    print(len(alotCells))

    # player cell ######################################################

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.moveForward()
        print("forward")
    if keys[pygame.K_a]:
        player.turnLeft()
        print("left")
    if keys[pygame.K_d]:
        player.turnRight()
        print("right")


    pygame.draw.rect(screen, "blue", (player.cords[0], player.cords[1], 3, 3))

    dt = clock.tick(10) / 1000.0 # limits FPS to n fps
    pygame.display.flip()
pygame.quit()




