import pygame
import random

SIM_WIDTH = 100
SIM_HEIGHT = 100
multiplier = 5

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []
        self.objectsCoordinates = [[None for _ in range(self.height)] for _ in range(self.width)]
        self.player = None

        self.lightMap = []
        self.generateLightMap()

    def update(self):
        for i in self.objects:
            i.update()

    def makeStep(self):
        self.update()

        alifeObjects = []
        for i in range(len(self.objects)):
            if self.objects[i].isAlife: alifeObjects.append(self.objects[i])
            else: self.objectsCoordinates[int(self.objects[i].cords[0])][int(self.objects[i].cords[1])]=None

        self.objects = alifeObjects

        self.playerMovement() # for testing and fun

    def generateLightMap(self):
        lMap = [[None for _ in range(self.height)] for _ in range(self.width)]
        for i in range(len(lMap)):
            for j in range(len(lMap[0])):
                #lMap[i][j] = i-j
                if i<len(lMap)//2: lMap[i][j] = (len(lMap)//2 - (len(lMap)//2-i))//4
                else: lMap[i][j] = (len(lMap)-i)//4
        self.lightMap = lMap
        #print(lMap)

    def playerMovement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.moveForward()
        if keys[pygame.K_a]:
            self.player.turnLeft()
        if keys[pygame.K_d]:
            self.player.turnRight()
        if keys[pygame.K_SPACE]:
            self.player.replicate()
        if keys[pygame.K_e]:
            self.player.biteCell()
        self.player.energy = 100

        if keys[pygame.K_UP]:
            if self.player.rotation == [0,-1]:
                self.player.moveForward()
            else: self.player.turnRight()
        if keys[pygame.K_RIGHT]:
            if self.player.rotation == [1,0]:
                self.player.moveForward()
            else: self.player.turnRight()
        if keys[pygame.K_DOWN]:
            if self.player.rotation == [0,1]:
                self.player.moveForward()
            else: self.player.turnRight()
        if keys[pygame.K_LEFT]:
            if self.player.rotation == [-1,0]:
                self.player.moveForward()
            else: self.player.turnRight()

    def isInBounds(self, x, y):
        if x<0 or y<0 or x>self.width-1 or y>self.height-1: return False
        else: return True

    def getObjectAt(self, x, y):
        if self.isInBounds(x, y) == False: return False
        else: return self.objectsCoordinates[x][y]
       
    def addObjectAt(self, x, y, obj):
        if self.getObjectAt(x, y)!=None:
            return
        obj.cords = [x, y]
        self.objectsCoordinates[x][y]=obj
        self.objects.append(obj)


world = World(SIM_WIDTH, SIM_HEIGHT)

class Cell:
    def __init__(self, cords, maxLifeTime=100, genome=None):
        self.cords = cords
        self.rotation = [1, 0]
        self.maxLifeTime = maxLifeTime
        self.lifeTime = maxLifeTime
        self.energy = 50
        self.isAlife = True

        if genome == None: self.genome = self.generateRandomGenome(16)
        else: self.genome = genome
        self.genomeStep = 0 # убрать потом?
        
        self.stepAmount = [0, 0, 0]
        for i in range(len(self.genome)):
            if 80 <= self.genome[i] < 100: self.stepAmount[0]+=1
            if 65 <= self.genome[i] < 80: self.stepAmount[1]+=1
            if self.genome[i] < 20: self.stepAmount[2]+=1



        #self.speed = speed # или max speed и speed выбирается отдельно
        #self.findRadius = None


    def update(self):
        self.makeStep()       
        self.energy-=1
        self.lifeTime-=1
        if self.energy<=0 or self.lifeTime==0: self.die()

    def die(self):
        self.isAlife = False

        #print("cell died, energy:", self.energy, "lifetime:", self.lifeTime)

    def makeStep(self):
        s = self.genome[self.genomeStep]
        if 0 <= s <20: 
            self.moveForward()
        if 20 <= s < 25: 
            self.turnLeft()
        if 25 <= s < 30: 
            self.turnRight()
        if 30 <= s < 50 and len(world.objects) < SIM_WIDTH*SIM_HEIGHT:
            self.replicate()
        if 50 <= s < 65:
            self.visuallyDependentBehavior()
        if 65 <= s < 80:
            self.photosynthesize()
        if 80 <= s < 100:
            self.biteCell()

        self.genomeStep+=1
        if self.genomeStep > len(self.genome)-1: self.genomeStep=0

    def moveForward(self):
        #сделать проверку на то заняты ли клетки между начальной и конечной (если добавить скорость)

        old_x = int(self.cords[0])
        old_y = int(self.cords[1])

        target_x = int(self.cords[0]+self.rotation[0])
        target_y = int(self.cords[1]+self.rotation[1])

        if world.isInBounds(target_x, target_y) == False: return

        if world.getObjectAt(target_x, target_y)!=None or False: return
        

        self.cords[0]=target_x
        self.cords[1]=target_y

        world.objectsCoordinates[int(self.cords[0])][int(self.cords[1])]=self
        world.objectsCoordinates[old_x][old_y]=None

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
        if self.energy<20:
            #print("not enough energy")
            return
        target_x = int(self.cords[0]+self.rotation[0])
        target_y = int(self.cords[1]+self.rotation[1])

        if world.isInBounds(target_x, target_y) == False: return

        if world.getObjectAt(target_x, target_y)!=None or False: return

        #print("new cell added")
        newGenome = self.genome.copy()
        for i in range(len(newGenome)):
            if random.randint(0,99)>94:
                newGenome[i]+=random.randint(-15,15)
            if newGenome[i]>100:newGenome[i] = newGenome[i]-100
            elif newGenome[i]<0:newGenome[i] = newGenome[i]+100

        newMaxLifeTime = self.maxLifeTime
        if random.randint(0,99)>90:
            newMaxLifeTime+=random.randint(-10,10)
        if newMaxLifeTime<=0: newMaxLifeTime=20

        newCell = Cell([self.cords[0]+self.rotation[0], self.cords[1]+self.rotation[1]], genome=newGenome, maxLifeTime=newMaxLifeTime)
        newCell.rotation = self.rotation

        newCell.energy = self.energy//2
        self.energy = self.energy//2

        world.addObjectAt(target_x, target_y, newCell)

    def generateRandomGenome(self, length): 
        return [random.randint(0,100) for _ in range(length)]

    def photosynthesize(self):
        self.energy+=world.lightMap[int(self.cords[0])][int(self.cords[1])]
        if self.energy>50: self.energy=50

    def biteCell(self):
        target_x = int(self.cords[0]+self.rotation[0])
        target_y = int(self.cords[1]+self.rotation[1])

        if world.isInBounds(target_x, target_y) == False: return

        if world.getObjectAt(target_x, target_y)==None or False: return

        target_cell = world.objectsCoordinates[int(target_x)][int(target_y)]
        if target_cell.energy<1:
            return

        self.energy+=target_cell.energy//2 
        target_cell.energy = target_cell.energy//2

    def visuallyDependentBehavior(self):
        target_x = self.cords[0]+self.rotation[0]
        target_y = self.cords[1]+self.rotation[1]
        if world.isInBounds(int(target_x), int(target_y)) == False: return

        if world.objectsCoordinates[int(target_x)][int(target_y)]==None:
            return
        else:
            for i in range(len(self.genome)//4):
                self.genomeStep+=1
                if self.genomeStep > len(self.genome)-1: self.genomeStep=0

class Sensor: # наследовать от cell / world?
    pass

class Actuator: # наследовать от cell / world?
    pass

visualMode = 0
def visuals():
    screen.fill((31, 31, 31))
    #for i in range(SIM_HEIGHT):
    #    pygame.draw.rect(screen, (i/SIM_HEIGHT*32, i/SIM_HEIGHT*32, i/SIM_HEIGHT*32), (0, i, SIM_WIDTH, 1))
    #pygame.draw.rect(screen, (127, 127, 127), (0, 0, SIM_WIDTH * multiplier, SIM_HEIGHT/3 * multiplier))
    #pygame.draw.rect(screen, (63, 63, 63), (0, SIM_HEIGHT/3 * multiplier, SIM_WIDTH * multiplier, SIM_HEIGHT/3 * multiplier))


    for i in world.objects:
        col = None
        if visualMode == 0: col = (255//len(i.genome)*i.stepAmount[0], 255//len(i.genome)*i.stepAmount[1], 255//len(i.genome)*i.stepAmount[2])
        if visualMode == 1: col = (255//len(i.genome)*i.stepAmount[0], 0, 0)
        if visualMode == 2: col = (0, 255//len(i.genome)*i.stepAmount[1], 0)
        if visualMode == 3: col = (0, 0, 255//len(i.genome)*i.stepAmount[2])
        if visualMode == 4: 
            if i.energy == 0: col = (0, 0, 0)
            elif i.energy > 255: col = (255, 255, 0)
            else: col = (i.energy, i.energy, 0)

        pygame.draw.rect(screen, col, (i.cords[0] * multiplier, i.cords[1] * multiplier, multiplier, multiplier))
    
    pygame.draw.rect(screen, "white", (world.player.cords[0] * multiplier, world.player.cords[1] * multiplier, multiplier, multiplier))


pygame.init()
screen = pygame.display.set_mode((SIM_WIDTH * multiplier, SIM_HEIGHT * multiplier))
clock = pygame.time.Clock()
running = True
dt = 0

world.objects = [Cell([random.randint(0, SIM_WIDTH-1), random.randint(0, SIM_HEIGHT-1)]) for _ in range(200)]
world.player = Cell([SIM_WIDTH//2, SIM_HEIGHT//2])
#world.player.genome = [...] # для порождения клеток с заданным геномом

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    world.makeStep()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_0]:
        visualMode = 0
    if keys[pygame.K_1]:
        visualMode = 1
    if keys[pygame.K_2]:
        visualMode = 2
    if keys[pygame.K_3]:
        visualMode = 3
    if keys[pygame.K_4]:
        visualMode = 4

    visuals()

    dt = clock.tick(1000) / 1000.0 # limits FPS to n fps
    pygame.display.flip()
pygame.quit()
