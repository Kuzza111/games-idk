import pygame
import random
import math


class Cell:
    def __init__(self, cords, lifeTime=500, color=None):
        self.cords = cords
        self.rotation = [1, 0]
        self.lifeTime = lifeTime
        self.energy = 50 # тратится на действие, если 0 - организм погибает
        self.isAlife = True

        self.genome = [random.randint(0,100) for _ in range(16)]
        #self.genome = self.generateGenome()
        self.genomeStep = 0 # убрать потом?
        
        if color==None: 
            self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        else: self.color = color

        #self.speed = speed # или max speed и speed выбирается отдельно
        #self.findRadius = None


    def update(self):
        self.makeStep()       
        self.energy-=1
        self.lifeTime-=1
        if self.energy==0 or self.lifeTime==0: 
            self.die()

    def makeStep(self):
        s = self.genome[self.genomeStep]
        if 0 <= s <25: 
            self.moveForward()
        if 25 <= s < 30: 
            self.turnLeft()
        if 30 <= s < 35: 
            self.turnRight()
        if 35 <= s < 65 and len(alotCells) < 1000:
            self.replicate()
        if 65 <= s < 90:
            self.getEnergy()
        
        self.genomeStep+=1
        if self.genomeStep > len(self.genome)-1: self.genomeStep=0

    def moveForward(self):
        #сделать проверку на возможность шага
            #клетка занята
                #клетки между начальной и конечной заняты

        # сделать шаг, заменить на ЗАПРОС шага, если можно - шаг
        self.cords[0]+=self.rotation[0]
        self.cords[1]+=self.rotation[1]

        # если за границей - переместиться, добавить проверку занята ли
        if self.cords[0]<0:self.cords[0]=screen.get_width()+self.cords[0]
        if self.cords[0]>=screen.get_width():self.cords[0]=self.cords[0]-screen.get_width()

        if self.cords[1]<0:self.cords[1]=screen.get_height()+self.cords[1]
        if self.cords[1]>=screen.get_height():self.cords[1]=self.cords[1]-screen.get_height()

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
        newCell = Cell([self.cords[0]+self.rotation[0], self.cords[1]+self.rotation[1]])
        newCell.rotation = self.rotation

        newGenome = self.genome.copy()
        for i in range(len(newGenome)):
            if random.randint(0,99)>98:
                newGenome[i]+=random.randint(-10,10)
            if newGenome[i]>100:newGenome[i] = newGenome[i]-100
            elif newGenome[i]<0:newGenome[i] = newGenome[i]+100
        newCell.genome = newGenome

        newLifeTime = self.lifeTime
        if random.randint(0,99)>50:
            newLifeTime+=random.randint(-100,100)
        if newLifeTime<=0: newLifeTime=50
        newCell.lifeTime = newLifeTime

        newCell.color = self.color

        alotCells.append(newCell)

    def die(self):
        self.isAlife = False

    def generateGenome(self): 
        for i in range(len(self.genome)):
            self.genome[i] = random.randint(0,100)

    def getEnergy(self):
        if (self.cords[1]<screen.get_height()/2 and self.cords[0]<screen.get_width()/2) or (self.cords[1]>screen.get_height()/2 and self.cords[0]>screen.get_width()/2) : # высота меньше т к счет начинается с левого верхнего угла, потому "сверху" это координаты меньше половины
                self.energy+=5
                if self.energy>100: self.energy=100




pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
running = True
dt = 0


alotCells = [Cell(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))) for _ in range(200)]
player = Cell([screen.get_width()/2, screen.get_height()/2])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((63, 63, 63))
    pygame.draw.rect(screen, (191, 191, 191), (0, 0, screen.get_width()/2, screen.get_height()/2))
    pygame.draw.rect(screen, (191, 191, 191), (screen.get_width()/2, screen.get_height()/2, screen.get_width()/2, screen.get_height()/2))


    # ai cells ######################################################
    for i in range(len(alotCells)):
        alotCells[i].update()

        if alotCells[i].isAlife: pygame.draw.rect(screen, alotCells[i].color, (alotCells[i].cords[0], alotCells[i].cords[1], 3, 3))

    alifeCells = []
    for i in range(len(alotCells)):
        if alotCells[i].isAlife: alifeCells.append(alotCells[i])
    alotCells = alifeCells
    if len(alotCells)==0: 
        print("all cells are dead, creating new")
        alotCells = [Cell(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))) for _ in range(200)]
    
    #print(len(alotCells))

    # player cell ######################################################

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.moveForward()
    if keys[pygame.K_a]:
        player.turnLeft()
    if keys[pygame.K_d]:
        player.turnRight()
    if keys[pygame.K_SPACE]:
        player.replicate()


    pygame.draw.rect(screen, "blue", (player.cords[0], player.cords[1], 3, 3))

    dt = clock.tick(100) / 1000.0 # limits FPS to n fps
    pygame.display.flip()
pygame.quit()
