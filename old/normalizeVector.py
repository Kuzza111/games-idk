import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True
dt = 0

target_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
start_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

def getDir(st, tar):
    linelenx = (tar[0] - st[0])
    lineleny = (tar[1] - st[1])
    lendia = (linelenx**2 + lineleny**2)**0.5
    
    x = 0
    y = 0
    if lendia != 0:
        x = linelenx / lendia
        y = lineleny / lendia

    return pygame.Vector2(x, y)




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dt = clock.tick(60) / 1000.0 # limits FPS to 60


        
    normalized = getDir(start_pos, target_pos)

    screen.fill("black")
    
    mouse = pygame.mouse.get_pressed()
    if mouse[0]: 
        print(f"sin: {normalized[1]}, cos: {normalized[0]}")
        pygame.draw.circle(screen, "red", target_pos, 5)
        pygame.draw.line(screen, "red", start_pos, target_pos)   
    
    pygame.draw.line(screen, "green", start_pos, (normalized[0] * 64 + screen.get_width() / 2, normalized[1] * 64 + screen.get_height() / 2))    
    
    target_pos = pygame.mouse.get_pos()

    pygame.display.flip()
pygame.quit()