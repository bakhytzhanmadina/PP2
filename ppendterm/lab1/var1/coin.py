import pygame
import random

pygame.init()
white = (255,255,255)
width = 800
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Points")

point = pygame.mixer.Sound("sound.wav")
back = pygame.image.load('back.jpeg')
back = pygame.transform.scale(back, (width, height))
trolley = pygame.image.load('trolley.png')
trolley = pygame.transform.scale(trolley,(250,200))
coin = pygame.image.load('coin.png')
coin = pygame.transform.scale(coin, (40,40))


class Player (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = trolley
        self.rect = self.image.get_rect()        
    def update(self):
        pos = pygame.mouse.get_pos()
        pos = pos[0]
        if pos>780:
            pos=780
        self.rect.x = pos-100
        self.rect.y = 420

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = coin
        self.rect = self.image.get_rect() 
    def reset_pos(self):
        self.rect.y = random.randrange(-300,-20)
        self.rect.x = random.randrange(0,width - 40)
    def update(self):
        self.rect.y += 4
        if self.rect.y > 600: 
            self.reset_pos()

ball_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group() #list of every sprite

for i in range(5):
        ball = Ball()
        ball.rect.x = random.randrange(0,width-40)
        ball.rect.y = random.randrange(-500,-10)
        ball_list.add(ball)
        all_sprites_list.add(ball)

player = Player()
all_sprites_list.add(player)#add player to the list

clock = pygame.time.Clock()
score = 0
n = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit  
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                raise SystemExit  
      
    if n==False:              #creating new coin after collision
        ball = Ball()
        ball.rect.x = random.randrange(0,width-40)
        ball.rect.y = random.randrange(-500,-10)
        ball_list.add(ball)
        all_sprites_list.add(ball)
        n = True
    
    

    all_sprites_list.update() 



    ball_hit_list = pygame.sprite.spritecollide(player, ball_list, True)  # collision
    for ball in ball_hit_list:
        score += 1
        point.play()
        n = False
        ball.reset_pos()
    
    screen.blit(back, (0, 0))
    
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Score: "+ str(score),True,(255,255,255))
    place = text.get_rect(center = (700,50))
    screen.blit(text,place)
      
    all_sprites_list.draw(screen)
    clock.tick(60)
    pygame.display.flip()
