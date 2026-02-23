import pygame
import random
import math
import copy


class Cell:
    def __init__(self, cords, lifeTime=100, color=None, genome=None):
        self.cords = cords
        cellsCoordinates[int(cords[0])][int(cords[1])] = self
        self.rotation = [1, 0]
        self.lifeTime = lifeTime
        self.energy = 50 # тратится на действие, если 0 - организм погибает
        self.isAlife = True

        if genome == None: self.genome = [random.randint(0,100) for _ in range(32)]
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
        if 30 <= s < 65 and len(alotCells) < SIM_WIDTH*SIM_HEIGHT:
            self.replicate()
        if 65 <= s < 100:
            self.getEnergy()
        
        self.genomeStep+=1
        if self.genomeStep > len(self.genome)-1: self.genomeStep=0

    def moveForward(self):
        #сделать проверку на то заняты ли клетки между начальной и конечной (если добавить скорость)

        old_x = self.cords[0]
        old_y = self.cords[1]

        target_x = self.cords[0]+self.rotation[0]
        target_y = self.cords[1]+self.rotation[1]

        if int(target_x)<0 or int(target_y)<0 or int(target_x)>SIM_WIDTH-1 or int(target_y)>SIM_HEIGHT-1: return

        if cellsCoordinates[int(target_x)][int(target_y)]!=None: return
        

        self.cords[0]=int(target_x)
        self.cords[1]=int(target_y)

        cellsCoordinates[int(self.cords[0])][int(self.cords[1])]=self
        cellsCoordinates[int(old_x)][int(old_y)]=None

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
        target_x = self.cords[0]+self.rotation[0]
        target_y = self.cords[1]+self.rotation[1]
        if int(target_x)<0 or int(target_y)<0 or int(target_x)>SIM_WIDTH-1 or int(target_y)>SIM_HEIGHT-1:
            return
        if cellsCoordinates[int(target_x)][int(target_y)]!=None:
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
        cellsCoordinates[int(self.cords[0])][int(self.cords[1])]=None

        #print("cell died, energy:", self.energy, "lifetime:", self.lifeTime)


    def generateGenome(self): 
        for i in range(len(self.genome)):
            self.genome[i] = random.randint(0,100)

    def getEnergy(self):
        if self.cords[1]<SIM_HEIGHT/3: self.energy+=25
        elif self.cords[1]<SIM_HEIGHT/3*2: self.energy+=15
        else: self.energy+=5
        if self.energy>50: self.energy=50

    

SIM_WIDTH = 150
SIM_HEIGHT = 100
multiplier = 10

pygame.init()
screen = pygame.display.set_mode((SIM_WIDTH * multiplier, SIM_HEIGHT * multiplier))
clock = pygame.time.Clock()
running = True
dt = 0

cellsCoordinates = [[None for _ in range(SIM_HEIGHT)] for _ in range(SIM_WIDTH)]
alotCells = [Cell(pygame.Vector2(random.randint(0, SIM_WIDTH-1), random.randint(0, SIM_HEIGHT-1))) for _ in range(200)]
player = Cell([SIM_WIDTH/2, SIM_HEIGHT/2])
#player.genome = [70, 60, 25, 20] # для порождения клеток с заданным геномом

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((31, 31, 31))
    #for i in range(SIM_HEIGHT):
    #    pygame.draw.rect(screen, (i/SIM_HEIGHT*32, i/SIM_HEIGHT*32, i/SIM_HEIGHT*32), (0, i, SIM_WIDTH, 1))
    pygame.draw.rect(screen, (127, 127, 127), (0, 0, SIM_WIDTH * multiplier, SIM_HEIGHT/3 * multiplier))
    pygame.draw.rect(screen, (63, 63, 63), (0, SIM_HEIGHT/3 * multiplier, SIM_WIDTH * multiplier, SIM_HEIGHT/3 * multiplier))

        



    # ai cells ######################################################
    alifeCells = []
    colorsOfCells = []

    for i in range(len(alotCells)):
        alotCells[i].update()

    for i in range(len(alotCells)):
        if alotCells[i].isAlife: 
            alifeCells.append(alotCells[i])
            colorsOfCells.append(alotCells[i].color)

    alotCells = alifeCells
    
    for i in range(len(alifeCells)):
        pygame.draw.rect(screen, alotCells[i].color, (alotCells[i].cords[0] * multiplier, alotCells[i].cords[1] * multiplier, multiplier, multiplier))

    #print("alotcells size: ", len(alotCells))

    if len(alotCells)==0:
        print("all cells are dead, resetting sim")
        playerCopy=copy.deepcopy(player)
        cellsCoordinates = [[None for _ in range(SIM_HEIGHT)] for _ in range(SIM_WIDTH)]
        alotCells = [Cell(pygame.Vector2(random.randint(0, SIM_WIDTH-1), random.randint(0, SIM_HEIGHT-1))) for _ in range(200)]
        player = playerCopy


    elif len(alotCells)>0:
        isAllCellsOneAncestor = True
        for i in range(len(colorsOfCells)):
            if colorsOfCells[i] != colorsOfCells[0]:
                isAllCellsOneAncestor = False
                break
    
        if isAllCellsOneAncestor==True:
            print(f"cell with color {colorsOfCells[0]} won, resetting sim with 1/3 population genome: {alifeCells[0].genome}")
            playerCopy=copy.deepcopy(player)
            cellsCoordinates = [[None for _ in range(SIM_HEIGHT)] for _ in range(SIM_WIDTH)]
            alotCells = [Cell(pygame.Vector2(random.randint(0, SIM_WIDTH-1), random.randint(0, SIM_HEIGHT-1)), genome=alifeCells[0].genome) for _ in range(50)]
            for i in range(100):
                alotCells.append(Cell(pygame.Vector2(random.randint(0, SIM_WIDTH-1), random.randint(0, SIM_HEIGHT-1))))
            player = playerCopy


    
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


    pygame.draw.rect(screen, "blue", (player.cords[0] * multiplier, player.cords[1] * multiplier, multiplier, multiplier))

    dt = clock.tick(100) / 1000.0 # limits FPS to n fps
    pygame.display.flip()
pygame.quit()
