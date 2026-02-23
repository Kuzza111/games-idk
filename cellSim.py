import pygame
import random
import math


class Cell:
    def __init__(self, cords, lifeTime=100, color=None, genome=None):
        self.cords = cords
        self.rotation = [1, 0]
        self.lifeTime = lifeTime
        self.energy = 50 # тратится на действие, если 0 - организм погибает
        self.isAlife = True

        if genome == None: self.genome = [random.randint(0,100) for _ in range(16)]
        else: self.genome = genome
        #self.genome = self.generateGenome()
        self.genomeStep = 0 # убрать потом?
        
        if color==None: self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        else: self.color = color

        #self.speed = speed # или max speed и speed выбирается отдельно
        #self.findRadius = None


    def update(self):
        self.makeStep()       
        self.energy-=1
        self.lifeTime-=1
        if self.energy<=0 or self.lifeTime==0: self.die()

    def makeStep(self):
        s = self.genome[self.genomeStep]
        if 0 <= s <20: 
            self.moveForward()
        if 20 <= s < 25: 
            self.turnLeft()
        if 25 <= s < 30: 
            self.turnRight()
        if 30 <= s < 65 and len(alotCells) < 1000:
            self.replicate()
        if 65 <= s < 100:
            self.getEnergy()
        
        self.genomeStep+=1
        if self.genomeStep > len(self.genome)-1: self.genomeStep=0

    def moveForward(self):
        #сделать проверку на возможность шага
            #клетка занята
                #клетки между начальной и конечной заняты

        # сделать шаг, заменить на ЗАПРОС шага, если можно - шаг
        for i in alotCells:
            if i.cords == [self.cords[0]+self.rotation[0], self.cords[1]+self.rotation[1]]:
                return
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
        if self.energy<30:
            #print("not enough energy")
            return
        for i in alotCells:
            if i.cords == [self.cords[0]+self.rotation[0], self.cords[1]+self.rotation[1]]:
                #self.turnLeft()
                #print("coordinates are not empty")
                return
        #print("new cell added")
        newGenome = self.genome.copy()
        for i in range(len(newGenome)):
            if random.randint(0,99)>94:
                newGenome[i]+=random.randint(-15,15)
            if newGenome[i]>100:newGenome[i] = newGenome[i]-100
            elif newGenome[i]<0:newGenome[i] = newGenome[i]+100

        newLifeTime = self.lifeTime
        if random.randint(0,99)>50:
            newLifeTime+=random.randint(-10,10)
        if newLifeTime<=0: newLifeTime=20

        newCell = Cell([self.cords[0]+self.rotation[0], self.cords[1]+self.rotation[1]], color=self.color, genome=newGenome, lifeTime=newLifeTime)
        newCell.rotation = self.rotation

        newCell.energy = self.energy//2
        self.energy = self.energy//2

        alotCells.append(newCell)

    def die(self):
        self.isAlife = False
        #print("cell died, energy:", self.energy, "lifetime:", self.lifeTime)


    def generateGenome(self): 
        for i in range(len(self.genome)):
            self.genome[i] = random.randint(0,100)

    def getEnergy(self):
        if self.cords[1]<screen.get_height()/2: 
            self.energy+=30
        if self.energy>50: self.energy=50

    



pygame.init()
screen = pygame.display.set_mode((500, 250))
clock = pygame.time.Clock()
running = True
dt = 0


alotCells = [Cell(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))) for _ in range(500)]
player = Cell([screen.get_width()/2, screen.get_height()/2])
#player.genome = [70, 60, 25, 20] # для порождения клеток с заданным геномом

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((31, 31, 31))
    #for i in range(screen.get_height()):
    #    pygame.draw.rect(screen, (i/screen.get_height()*32, i/screen.get_height()*32, i/screen.get_height()*32), (0, i, screen.get_width(), 1))
    pygame.draw.rect(screen, (127, 127, 127), (0, 0, screen.get_width(), screen.get_height()/2))
        



    # ai cells ######################################################
    alifeCells = []
    colorsOfCells = []

    for i in range(len(alotCells)):
        alotCells[i].update()

    for i in range(len(alotCells)):
        if alotCells[i].isAlife: 
            alifeCells.append(alotCells[i])
            colorsOfCells.append(alotCells[i].color)
            pygame.draw.rect(screen, alotCells[i].color, (alotCells[i].cords[0], alotCells[i].cords[1], 3, 3))

    alotCells = alifeCells
    
    #print("alotcells size: ", len(alotCells))

    if len(alotCells)==0:
        print("all cells are dead, resetting sim")
        alotCells = [Cell(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))) for _ in range(200)]

    elif len(alotCells)>0:
        isAllCellsOneAncestor = True
        for i in range(len(colorsOfCells)):
            if colorsOfCells[i] != colorsOfCells[0]:
                isAllCellsOneAncestor = False
                break
    
        if isAllCellsOneAncestor==True:
            print(f"cell with color {colorsOfCells[0]} won, resetting sim with half population genome: {alifeCells[0].genome}")
            alotCells = [Cell(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())), genome=alifeCells[0].genome) for _ in range(100)]
            for i in range(100):
                alotCells.append(Cell(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))))


    
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
    player.energy = 100


    pygame.draw.rect(screen, "blue", (player.cords[0], player.cords[1], 3, 3))

    dt = clock.tick(1000) / 1000.0 # limits FPS to n fps
    pygame.display.flip()
pygame.quit()
