import pygame
import random
import math


class Cell:
    def __init__(self, cords, speed, lifeTime=100):
        self.cords = cords
        self.rotation = [1, 0]

        #self.speed = speed
        #self.lifeTime = lifeTime
        #self.findRadius = None

    def makeStep(self):
        #сделать проверку на возможность шага
        self.cords[0]+=self.rotation[0]
        self.cords[1]+=self.rotation[1]

        if alotCells[i].cords[0]<0:alotCells[i].cords[0]=screen.get_width()+alotCells[i].cords[0]
        if alotCells[i].cords[0]>screen.get_width():alotCells[i].cords[0]=alotCells[i].cords[0]-screen.get_width()

        if alotCells[i].cords[1]<0:alotCells[i].cords[1]=screen.get_height()+alotCells[i].cords[1]
        if alotCells[i].cords[1]>screen.get_height():alotCells[i].cords[1]=alotCells[i].cords[1]-screen.get_height()

    def turnRight(self):
        if self.rotation==[1,0]:self.rotation=[0,-1]
        elif self.rotation==[0,-1]: self.rotation=[-1,0]
        elif self.rotation==[-1,0]: self.rotation=[0,1]
        elif self.rotation==[0,1]: self.rotation=[1,0]

    def turnLeft(self):
        if self.rotation==[1,0]:self.rotation=[0,-1]
        elif self.rotation==[0,-1]: self.rotation=[-1,0]
        elif self.rotation==[-1,0]: self.rotation=[0,1]
        elif self.rotation==[0,1]: self.rotation=[1,0]

pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
running = True
dt = 0


alotCells = [Cell(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())), 1) for _ in range(1000)]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")



    for i in range(len(alotCells)):
        alotCells[i].makeStep()
        if random.randint(0, 99)>98:
            if random.randint(0, 1)==0: alotCells[i].turnLeft()
            else: alotCells[i].turnRight()


        pygame.draw.rect(screen, "red", (alotCells[i].cords[0], alotCells[i].cords[1], 1, 1))


    dt = clock.tick(10) / 1000.0 # limits FPS to 60
    pygame.display.flip()
pygame.quit()




#    keys = pygame.key.get_pressed()
#    if keys[pygame.K_a]:
#        cords[0] -= speed
#    if keys[pygame.K_d]:
#        cords[0] += speed
#    if keys[pygame.K_w]:
#        cords[1] -= speed
#    if keys[pygame.K_s]:
#        cords[1] += speed