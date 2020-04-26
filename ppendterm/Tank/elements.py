import pygame
import random
import time
from enum import Enum
pygame.init()
screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((screenwidth,screenheight))


font = pygame.font.SysFont('Arial', 32) 

pygame.mixer.music.load('start.wav')
pygame.mixer.music.play(1)
pygame.mixer.music.set_volume(0.05)
bulletSound=pygame.mixer.Sound('bullet_shot.wav')
explosionSound=pygame.mixer.Sound('explosion.wav')

white = (255,255,255)
black = (0,0,0)
grey = (192,192,192)

red = (200,0,0)
light_red = (255,0,0)
med_red = (255, 153, 51)

green = (34,177,76)
light_green = (0,255,0)
med_green = (47, 116,127)

yellow = (200,200,0)
light_yellow = (255,255,0)

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)

def message_to_screen(msg,color,y_displace=0,size="small"):
    textSurf,textRect = text_objects(msg,color,size)
    textRect.center = (int(screenwidth/2),int(screenheight/2)+y_displace)
    screen.blit(textSurf, textRect)  

def text_objects(text,color,size="small"):
    if size == 'small':
        textSurface = smallfont.render(text, 1, color)
    if size == "medium":
        textSurface = medfont.render(text, 1, color)
    if size == "large":
        textSurface = largefont.render(text, 1, color)
    return textSurface, textSurface.get_rect()  


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Tank:
    def __init__(self, x, y, speed, color, right=pygame.K_RIGHT, left=pygame.K_LEFT, up=pygame.K_UP, down=pygame.K_DOWN,pull=pygame.K_RETURN):
        self.x = x
        self.y = y
        self.lives=3
        self.speed = speed
        self.color = color
        self.width = 40
        self.direction = Direction.RIGHT
        self.KEY = {right: Direction.RIGHT, left: Direction.LEFT,
                    up: Direction.UP, down: Direction.DOWN}
        self.shoot=pull

    def draw(self):
        center = (self.x + int(self.width / 2), self.y + int(self.width / 2))
        pygame.draw.rect(screen,self.color,(self.x,self.y,self.width,self.width),8)
        pygame.draw.circle(screen,self.color,center, int(self.width / 3))

        if self.direction == Direction.RIGHT:
            pygame.draw.line(screen,self.color, center, (self.x + self.width + int(self.width /2), self.y  + int(self.width /2 )),4)
        if self.direction == Direction.LEFT:
            pygame.draw.line(screen,self.color, center, (self.x - int(self.width /2), self.y + int(self.width /2 )),4)
        if self.direction == Direction.UP:
            pygame.draw.line(screen,self.color, center, (self.x + int(self.width /2), self.y - int(self.width /2 )),4)
        if self.direction == Direction.DOWN:
            pygame.draw.line(screen,self.color, center, (self.x + int(self.width /2), self.y + self.width + int(self.width /2 )),4)

    def SetDir(self,direction):
        self.direction = direction

    def move(self):
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        #infinite field    
        if self.x > 800:     
            self.x = 0 - self.width  
        if self.x < 0 - self.width:           
            self.x = 800
        if self.y > 600:
            self.y = 0 - self.width
        if self.y < 0 - self.width:
            self.y = 600

        self.draw()
    
class Bullet:
    def __init__(self,x=0,y=0,color=(0,0,0),direction=Direction.LEFT,speed=10):
        self.x=x
        self.y=y
        self.color=color
        self.speed=speed
        self.state=True
        self.direction=direction
        self.distance=0
        self.radius=10

    def move(self):
        if self.direction == Direction.RIGHT:
            self.x += self.speed
        if self.direction == Direction.LEFT:
            self.x -= self.speed
        if self.direction == Direction.UP:
            self.y -= self.speed
        if self.direction == Direction.DOWN:
            self.y += self.speed
        self.distance+=1
        if self.distance>(2*800):
            self.state=False
        self.draw()

    def draw(self):
        if self.state:
            pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)

def collision():
    for bul in bullet:
        for tank in tanks:
            if (tank.x-bul.radius < bul.x <tank.x+bul.radius+40)and (tank.y-bul.radius < bul.y < tank.y+bul.radius+40) and bul.state==True:
                explosionSound.play()
                bul.color=(0,0,0)
                tank.lives -= 1
                bul.state=False
                
                tank.x=random.randint(50,screenwidth-70)
                tank.y=random.randint(50,screenheight-70)

            if tank.lives == 0:
                message_to_screen("Game Over",red,-50,size="large") 
                message_to_screen("Press C to play again",black,50)
                tank1.x = screenwidth - 140
                tank1.y = 380
                tank1.speed = 0
                tank2.x = 100
                tank2.y = 380
                tank2.speed = 0
                key = pygame.key.get_pressed()
                if key[pygame.K_c]:
                    tank.lives = 3
                    tank1.speed = tank2.speed = 4
                    tank1.x = random.randint(50,screenwidth - 70)
                    tank1.y = random.randint(50,screenheight - 70)
                    tank2.x = random.randint(50,screenwidth - 70)
                    tank2.y = random.randint(50,screenheight - 70)
                
              

def life_count():
    score1= tanks[1].lives
    score2= tanks[0].lives
    tank12 = font.render(str(score2), 1, (255, 102, 0))
    tank22 = font.render(str(score1), 1, (47, 116,127))
    
    screen.blit(tank22, (30,30))
    screen.blit(tank12, (750,30))

def pause():
    paused = True
    message_to_screen("Paused",red,-100,size="large")
    message_to_screen("Press C to continue, Q to quit",black,25)
    while paused:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.flip()
        clock.tick(5)
                
def SetCoord(tank):
    if tank.direction == Direction.RIGHT:
        x=tank.x + 60
        y=tank.y + 20

    if tank.direction == Direction.LEFT:
        x=tank.x - 20
        y=tank.y + 20

    if tank.direction == Direction.UP:
        x=tank.x + 20
        y=tank.y - 20

    if tank.direction == Direction.DOWN:
        x=tank.x + 20
        y=tank.y + 60
    bul=Bullet(x,y,tank.color,tank.direction)
    bullet.append(bul)



tank1 = Tank(200,200,4,(255,102,0),pygame.K_RIGHT,pygame.K_LEFT, pygame.K_UP,pygame.K_DOWN,pygame.K_RETURN)
tank2 = Tank(100,100,4,(47, 116,127),pygame.K_d,pygame.K_a,pygame.K_w,pygame.K_s,pygame.K_SPACE)
bullet1=Bullet()
bullet2=Bullet()
tanks = [tank1, tank2]
bullet = [bullet1, bullet2]

def run():
    clock = pygame.time.Clock()
    FPS = 60
    mainloop = True
    while mainloop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:
                    pause()
                pressed = pygame.key.get_pressed()
                for tank in tanks:
	                if event.key in tank.KEY.keys():
	                    tank.SetDir(tank.KEY[event.key])
	                if event.key in tank.KEY.keys():
	                    tank.move()
	                if pressed[tank.shoot]:
	                    bulletSound.play()
	                    SetCoord(tank)
        clock.tick(FPS)           
        screen.fill((230,230,250)) 
        life_count()
        collision()
        for bul in bullet:
            bul.move()
        for tank in tanks:
            tank.draw()
        tank1.move()
        tank2.move()
        pygame.display.flip()  
		   
