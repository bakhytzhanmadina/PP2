import pygame

pygame.init()

screen = pygame.display.set_mode((800,600))

background = pygame.Surface(screen.get_size())
background.fill((255,255,255))
background = background.convert() #convert the pygame.Surface to the same pixel

screenrect = screen.get_rect()

ballsurface = pygame.Surface((50,50))        
ballsurface.set_colorkey((0,0,0))         
pygame.draw.circle(ballsurface, (255,0,0), (25,25),25)        
ballrect = ballsurface.get_rect()        
ballsurface = ballsurface.convert_alpha()          
ballx, bally = 100,100                         

screen.blit(background,(0,0))
screen.blit(ballsurface, (ballx, bally))

speed = 20

clock = pygame.time.Clock()

running = True
FPS = 50
while running:
    milliseconds = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LEFT]:
        ballx=ballx-speed
    if keys[pygame.K_RIGHT]:
        ballx=ballx+speed
    if keys[pygame.K_UP]:
        bally=bally-speed        
    if keys[pygame.K_DOWN]: 
        bally=bally+speed
    if ballx < 0:
        ballx = 0    
    elif ballx + ballrect.width > screenrect.width:
        ballx = screenrect.width - ballrect.width
    if bally < 0:
        bally = 0
    elif bally + ballrect.height > screenrect.height:
        bally = screenrect.height - ballrect.height    
    screen.blit(background,(0,0))    
    screen.blit(ballsurface, (ballx, bally))
    pygame.display.flip()
    

pygame.quit()
