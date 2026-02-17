import pygame
import random
import math


class Cell:
    def __init__(self, cords, speed, lifeTime=100):
        self.cords = cords
        self.speed = speed
        self.lifeTime = lifeTime
        self.findRadius = None


pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
running = True
dt = 0


alotCells = [Cell(pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())), 1) for _ in range(10)]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    for i in range(len(alotCells)):
        if alotCells[i].speed > 0:
            alotCells[i].cords[0]+=alotCells[i].speed
            alotCells[i].cords[1]+=random.randint(-alotCells[i].speed, alotCells[i].speed)

        if alotCells[i].cords[0]<0:alotCells[i].cords[0]=screen.get_width()+alotCells[i].cords[0]
        if alotCells[i].cords[0]>screen.get_width():alotCells[i].cords[0]=alotCells[i].cords[0]-screen.get_width()

        if alotCells[i].cords[1]<0:alotCells[i].cords[1]=screen.get_height()+alotCells[i].cords[1]
        if alotCells[i].cords[1]>screen.get_height():alotCells[i].cords[1]=alotCells[i].cords[1]-screen.get_height()


        if random.randint(0, 99) == 99:
            if alotCells[i].speed > 0:
                if len(alotCells) < 5000:
                    newc = pygame.Vector2(alotCells[i].cords[0]-1, alotCells[i].cords[1] + random.randint(-alotCells[i].speed, alotCells[i].speed))
                    news = alotCells[i].speed + random.randint(-1, 1)
                    newlt = alotCells[i].lifeTime + random.randint(-10, 10)
                    alotCells.append(Cell(newc, news, lifeTime=newlt))

        #alotCells[i].lifeTime -= 1
        #if alotCells[i].lifeTime == 0:
            #alotCells[i] == None
            #alotCells.pop(i)



    for i in range(len(alotCells)):
        if alotCells[i].speed == 0:
            pygame.draw.rect(screen, "blue", (alotCells[i].cords[0], alotCells[i].cords[1], 1, 1))
        else:
            pygame.draw.rect(screen, "red", (alotCells[i].cords[0], alotCells[i].cords[1], 1, 1))



    dt = clock.tick(100) / 1000.0 # limits FPS to 60

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