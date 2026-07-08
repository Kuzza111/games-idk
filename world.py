import pygame
class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.objects = []
        self.objectsCoordinates = [[None for _ in range(self.height)] for _ in range(self.width)]
        self.player = None # delete later, make player just a cell

        self.lightMap = []
        self.generateLightMap()

    def update(self):
        for i in self.objects:
            i.update()
            if not i.isAlife: self.removeObjectAt(i.cords[0], i.cords[1])
        
        self.playerMovement() # for testing and fun, delete later

    def generateLightMap(self):
        lMap = [[10 for _ in range(self.height)] for _ in range(self.width)]
        for i in range(len(lMap)):
            for j in range(len(lMap[0])):
                lMap[i][j] = i-j
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
            self.player.removeCell()
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

    def removeObjectAt(self, x, y):
        obj = self.getObjectAt(x, y)
        if obj!=None: 
            self.objectsCoordinates[x][y]=None
            if obj in self.objects:
                self.objects.remove(obj)

#    def getObject(self, obj)? 