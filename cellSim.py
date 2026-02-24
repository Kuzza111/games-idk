import pygame
import random

SIM_WIDTH = 75
SIM_HEIGHT = 75
multiplier = 5

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []
        self.objectsCoordinates = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.player = None

        self.lightMap = []
        self.generateLightMap()

    def update(self):
        for i in range(len(self.objects)):
            self.objects[i].update()

    def makeStep(self):
        self.update()

        alifeObjects = []
        for i in range(len(self.objects)):
            if self.objects[i].isAlife: 
                alifeObjects.append(self.objects[i])
        self.objects = alifeObjects

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.moveForward()
        if keys[pygame.K_a]:
            self.player.turnLeft()
        if keys[pygame.K_d]:
            self.player.turnRight()
        if keys[pygame.K_SPACE]:
            self.player.replicate()
        self.player.energy = 100

    def generateLightMap(self):
        lMap = [[None for _ in range(self.height)] for _ in range(self.width)]
        for i in range(len(lMap)):
            for j in range(len(lMap[0])):
                lMap[i][j] = (i + j)//6#int(self.height/i)
        self.lightMap = lMap
        print(self.lightMap)
        print(len(self.lightMap), " ", len(self.lightMap[0]))

world = World(SIM_WIDTH, SIM_HEIGHT)
world.objectsCoordinates = [[None for _ in range(SIM_HEIGHT)] for _ in range(SIM_WIDTH)]


class Cell:
    def __init__(self, cords, lifeTime=100, genome=None):
        self.cords = cords
        world.objectsCoordinates[int(cords[0])][int(cords[1])] = self
        self.rotation = [1, 0]
        self.lifeTime = lifeTime
        self.energy = 50 # тратится на действие, если 0 - организм погибает
        self.isAlife = True

        if genome == None: self.genome = self.generateRandomGenome(16)
        else: self.genome = genome
        #self.genome = self.generateGenome()
        self.genomeStep = 0 # убрать потом?
        
        blue = 0
        for i in range(len(self.genome)):
            if self.genome[i] < 20:
                blue+=1
        red = 0
        for i in range(len(self.genome)):
            if 80 <= self.genome[i] < 100:
                red+=1
        green = 0
        for i in range(len(self.genome)):
            if 65 <= self.genome[i] < 80:
                green+=1
        self.color = (255//len(self.genome)*red, 255//len(self.genome)*green, 255//len(self.genome)*blue)


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
        if 30 <= s < 65 and len(world.objects) < SIM_WIDTH*SIM_HEIGHT:
            self.replicate()
        if 65 <= s < 80:
            self.photosynthesize()
        if 80 <= s < 100:
            self.biteCell()

        self.genomeStep+=1
        if self.genomeStep > len(self.genome)-1: self.genomeStep=0

    def moveForward(self):
        #сделать проверку на то заняты ли клетки между начальной и конечной (если добавить скорость)

        old_x = self.cords[0]
        old_y = self.cords[1]

        target_x = self.cords[0]+self.rotation[0]
        target_y = self.cords[1]+self.rotation[1]

        if int(target_x)<0 or int(target_y)<0 or int(target_x)>SIM_WIDTH-1 or int(target_y)>SIM_HEIGHT-1: return

        if world.objectsCoordinates[int(target_x)][int(target_y)]!=None: return
        

        self.cords[0]=int(target_x)
        self.cords[1]=int(target_y)

        world.objectsCoordinates[int(self.cords[0])][int(self.cords[1])]=self
        world.objectsCoordinates[int(old_x)][int(old_y)]=None

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
        if world.objectsCoordinates[int(target_x)][int(target_y)]!=None:
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

        newCell = Cell([self.cords[0]+self.rotation[0], self.cords[1]+self.rotation[1]], genome=newGenome, lifeTime=newLifeTime)
        newCell.rotation = self.rotation

        newCell.energy = self.energy//2
        self.energy = self.energy//2

        world.objects.append(newCell)

    def die(self):
        self.isAlife = False
        world.objectsCoordinates[int(self.cords[0])][int(self.cords[1])]=None

        #print("cell died, energy:", self.energy, "lifetime:", self.lifeTime)


    def generateRandomGenome(self, length): 
        return [random.randint(0,100) for _ in range(length)]

    def photosynthesize(self):
        self.energy+=world.lightMap[int(self.cords[0])][int(self.cords[1])]
        if self.energy>50: self.energy=50

    def biteCell(self):
        target_x = self.cords[0]+self.rotation[0]
        target_y = self.cords[1]+self.rotation[1]
        if int(target_x)<0 or int(target_y)<0 or int(target_x)>SIM_WIDTH-1 or int(target_y)>SIM_HEIGHT-1:
            return
        if world.objectsCoordinates[int(target_x)][int(target_y)]==None:
            return
        target_cell = world.objectsCoordinates[int(target_x)][int(target_y)]
        if target_cell.energy<10:
            return

        target_cell.energy-=10
        self.energy+=10


pygame.init()
screen = pygame.display.set_mode((SIM_WIDTH * multiplier, SIM_HEIGHT * multiplier))
clock = pygame.time.Clock()
running = True
dt = 0

world.objects = [Cell(pygame.Vector2(random.randint(0, SIM_WIDTH-1), random.randint(0, SIM_HEIGHT-1))) for _ in range(200)]
world.player = Cell([SIM_WIDTH/2, SIM_HEIGHT/2])
#world.player.genome = [...] # для порождения клеток с заданным геномом

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((31, 31, 31))
    #for i in range(SIM_HEIGHT):
    #    pygame.draw.rect(screen, (i/SIM_HEIGHT*32, i/SIM_HEIGHT*32, i/SIM_HEIGHT*32), (0, i, SIM_WIDTH, 1))
    #pygame.draw.rect(screen, (127, 127, 127), (0, 0, SIM_WIDTH * multiplier, SIM_HEIGHT/3 * multiplier))
    #pygame.draw.rect(screen, (63, 63, 63), (0, SIM_HEIGHT/3 * multiplier, SIM_WIDTH * multiplier, SIM_HEIGHT/3 * multiplier))


    world.makeStep()

    for i in range(len(world.objects)):
        pygame.draw.rect(screen, world.objects[i].color, (world.objects[i].cords[0] * multiplier, world.objects[i].cords[1] * multiplier, multiplier, multiplier))
    pygame.draw.rect(screen, "blue", (world.player.cords[0] * multiplier, world.player.cords[1] * multiplier, multiplier, multiplier))

    dt = clock.tick(1000) / 1000.0 # limits FPS to n fps
    pygame.display.flip()
pygame.quit()
