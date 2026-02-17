import pygame
import random
import math

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1000, 500))
clock = pygame.time.Clock()
running = True
dt = 0

speed = 5

cords = pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height()))

alotcords = [pygame.Vector2(random.randint(0, screen.get_width()), random.randint(0, screen.get_height())) for _ in range(1000)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    for i in alotcords:
        i[0] += random.randint(-10, 10)
        if i[0]<0:i[0]=screen.get_width()+i[0]
        if i[0]>screen.get_width():i[0]=i[0]-screen.get_width()

        i[1] += random.randint(-10, 10)
        if i[1]<0:i[1]=screen.get_height()+i[1]
        if i[1]>screen.get_height():i[1]=i[1]-screen.get_height()

        pos = pygame.mouse.get_pos()
        color = "red"
        if math.hypot(i[0] - pos[0], i[1] - pos[1]) < 100:
            color = "green"
            pygame.draw.line(screen, "blue", i, pos)
            if i[0]<pos[0]:i[0]-=2
            if i[0]>pos[0]:i[0]+=2

            if i[1]<pos[1]:i[1]-=2
            if i[1]>pos[1]:i[1]+=2

        if 150 < math.hypot(i[0] - pos[0], i[1] - pos[1]) < 200:
            color = "green"
            pygame.draw.line(screen, "blue", i, pos)
            if i[0]<pos[0]:i[0]+=2
            if i[0]>pos[0]:i[0]-=2

            if i[1]<pos[1]:i[1]+=2
            if i[1]>pos[1]:i[1]-=2

        pygame.draw.circle(screen, color, i, 3)

    pygame.draw.circle(screen, "grey", pygame.mouse.get_pos(), 100, 1)
    pygame.draw.circle(screen, "blue", pygame.mouse.get_pos(), 150, 1)
    pygame.draw.circle(screen, "grey", pygame.mouse.get_pos(), 200, 1)

    dt = clock.tick(60) / 1000.0 # limits FPS to 60

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