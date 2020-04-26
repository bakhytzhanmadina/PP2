import pygame
import random
import elements as game

pygame.init()

screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((screenwidth,screenheight))
pygame.display.set_caption('Tanks')
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

FPS = 60
clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 32) 

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)

def button(text,x,y,width,height,inactive_color,active_color,action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < cur[0] < x + width and y < cur[1] < y + height:
        pygame.draw.rect(screen,active_color,(x,y,width,height))
        if click[0] == 1 and action != None:
            if action == "play":
                loading()
            if action == "controls":
                game_controls()
            if action == "quit":
                pygame.quit()
                quit()
            
    else:
        pygame.draw.rect(screen,inactive_color,(x,y,width,height))
    text_to_button(text,black,x,y,width,height)

def text_to_button(msg,color,buttonx,buttony,buttonwidth,buttonheight, size="small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+int(buttonwidth/2)),buttony+int(buttonheight/2))
    screen.blit(textSurf,textRect)

def text_objects(text,color,size="small"):
    if size == 'small':
        textSurface = smallfont.render(text, 1, color)
    if size == "medium":
        textSurface = medfont.render(text, 1, color)
    if size == "large":
        textSurface = largefont.render(text, 1, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size="small"):
    textSurf,textRect = text_objects(msg,color,size)
    textRect.center = (int(screenwidth/2),int(screenheight/2)+y_displace)
    screen.blit(textSurf, textRect)

def game_controls():
    cont = True
    while cont:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(med_red)
        message_to_screen("Controls",med_green,-100,size="large")
        message_to_screen("Move Player1: Up,Down,Right and Left arrows",black,-30)
        message_to_screen("Fire: Spacebar",black,10)
        message_to_screen("Move Player2: W,S,D ana A keyboard keys",black,50)
        message_to_screen("Fire: Enter",black,90)
        message_to_screen("Pause: P",black,130)
        
        button("play",150,500,100,50,green,light_green,action="play")
        button("quit",550,500,100,50,red,light_red,action="quit")

        pygame.display.flip()
        clock.tick(15)

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro = False
        screen.fill(med_green)
        message_to_screen("Welcome to Tanks!",med_red,-100,size="large")

        button("play",150,370,100,50,green,light_green,action="play")
        button("controls",350,370,100,50,yellow,light_yellow,action="controls")
        button("quit",550,370,100,50,red,light_red,action="quit")

        pygame.display.flip()
        clock.tick(FPS)

def loading():   
    font = pygame.font.SysFont("Arial",32)
    game_tip = font.render('Game is loading',1,(med_green))
    game_tip_rect = game_tip.get_rect()
    game_tip_rect.centerx, game_tip_rect.top = int(screenwidth/2), int(screenheight/2)
    game_tip_flash_time = 25
    game_tip_flash_count = 0 
    game_tip_show_flag = True
  

    font1 = pygame.font.Font('font/font.TTF', int(screenheight//6))
    font1_render = font1.render('Tank Battle',1,(med_green))
    font1_rect = font1_render.get_rect()
    font1_rect.centerx, font1_rect.centery = int(screenwidth/2),int(screenheight/4)
 
    gamebar = pygame.image.load('gamebar.png').convert_alpha()
    gamebar_rect = gamebar.get_rect()
    gamebar_rect.centerx, gamebar_rect.centery = int(screenwidth/2), int(screenheight/1.4)

    tank_curs = pygame.image.load('tank.png').convert_alpha()
    tank_curs = pygame.transform.scale(tank_curs,(48,48))
    
    tank_rect = tank_curs.get_rect()
    tank_rect.left = gamebar_rect.left
    tank_rect.centery = gamebar_rect.centery
    load_time_left = gamebar_rect.right - tank_rect.right
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if load_time_left <= 0:
            gameloop()
        screen.fill((med_red))
        game_tip_flash_count += 1
        if game_tip_flash_count > game_tip_flash_time:
            game_tip_show_flag = not game_tip_show_flag
            game_tip_flash_count = 0
        if game_tip_show_flag:
            screen.blit(game_tip,game_tip_rect)
        
        screen.blit(font1_render, font1_rect)
        screen.blit(gamebar,gamebar_rect)
        screen.blit(tank_curs,tank_rect)
        pygame.draw.rect(screen,grey,(gamebar_rect.left+8,gamebar_rect.top+8,tank_rect.left-gamebar_rect.left-8,tank_rect.bottom-gamebar_rect.top-16))
        tank_rect.left += 1
        load_time_left -= 1
        pygame.display.flip()
        clock.tick(FPS)

def gameloop():
    game.run()
    
game_intro()