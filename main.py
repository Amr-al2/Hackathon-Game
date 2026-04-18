import pygame
import math
import random
import os
import time
from player_class import player
from obstacles import obstacle
pygame.init()

#Set Up Screen
W, H = 1000, 700
WIN = pygame.display.set_mode((W, H))
display = pygame.Surface((W // 2, H // 2))
pygame.display.set_caption("Hackathon")
pygame.mouse.set_visible(False)

#FPS
FPS = 60

#Varibles
last_time = time.time()

start = False
current_time = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()

##Shoot
shoot_cd = 1
bullets = []

#Movement
up = False
down = False
left = False
right = False
vel = 150

dirc = ["right"]
dash = False
dash_count = 0
dash_allow = True
dash_cd = 1

#Colors
black = (0,0,0)
white = (255,255,255)

colors = [(255,255,255), (0,0,0), (255,255,255)]

#Images
def loadify(imgname):
    return pygame.image.load(os.path.join(imgname)).convert_alpha()

ss_img = loadify("space_ship.png")

#Pixel Font
def clip(surf,x,y,x_size,y_size):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x,y,x_size,y_size)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        font_img = loadify(path).convert()
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing

my_big_font = Font('large_font.png')

#Shoot
def make_bullet(rect):
    bullet = pygame.FRect(rect.right + 5, rect.bottom - rect.height // 2 - 2, 12, 4)
    return bullet

#Rects

##Astroids
astroids_max = 8
astroid_cd = pygame.time.get_ticks()
astroidRect = pygame.FRect(W // 2 + 10, 0, 25, 25)
astroids = []

##Borders
tiles = [pygame.Rect(0, 0 - 50, W // 2, 50), pygame.Rect(0 - 50, 0, 50, H // 2), pygame.Rect(0, H // 2, W // 2, 50), pygame.Rect(W // 2, 0, 50, H // 2)]

##BG
bgs = [pygame.FRect(0, 0, W // 2, H // 2), pygame.FRect(W // 2, 0, W // 2, H // 2), pygame.FRect(W, 0, W // 2, H // 2)]

bg_blocker = pygame.Rect(-W // 2 - 100 // 2, 0, 100 // 2, H // 2)

#Player
p = player(W // 4, H // 4, 20, 16)

#Collision Detection

#Game Loop
clock = pygame.time.Clock()
run = True
while run:

    #Time Tracker
    if start == True:
      current_time = pygame.time.get_ticks()
    #Delta Time
    dt = clock.tick(FPS) / 1000
    last_time = time.time()

    display.fill(black)
    num = 0
    for bg in bgs:
      break
      if bg.colliderect(bg_blocker):
       bg.x = W
      pygame.draw.rect(display, colors[num], bg)
      bg.x -= 200 * dt
      num += 1

    movement = [0,0]

    if up:
       movement[1] -= vel * dt
    if down: 
       movement[1] += vel * dt
    if right:
       movement[0] += vel * dt
    if left:
       movement[0] -= vel * dt 

    if dash_count + 1 >= 5:
      dash = False
      dash_count = 0

    if dash:
       if dirc[-1] == "up":
          movement[1] -= dash_count * 5
          dash_count += 0.5

       if dirc[-1] == "down":
          movement[1] += dash_count * 5
          dash_count += 0.5

       if dirc[-1] == "left":
          movement[0] -= dash_count * 5
          dash_count += 0.5

       if dirc[-1] == "right":
          movement[0] += dash_count * 5
          dash_count += 0.5 

       if dirc[-1] == "rightUp":
          movement[0] += dash_count * 5
          movement[1] -= dash_count * 5
          dash_count += 0.5

       if dirc[-1] == "rightDown":
          movement[0] += dash_count * 5
          movement[1] += dash_count * 5
          dash_count += 0.5

       if dirc[-1] == "leftUp":
          movement[0] -= dash_count * 5
          movement[1] -= dash_count * 5
          dash_count += 0.5

       if dirc[-1] == "leftDown":
          movement[0] -= dash_count * 5
          movement[1] += dash_count * 5
          dash_count += 0.5      
       
    p.rect = p.move(p.rect, movement, tiles)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_w:
              up = True
              dirc.append("up")
              if right:
                 dirc.append("rightUp")
              if left:
                 dirc.append("leftUp")   
           if event.key == pygame.K_s:
              down = True
              dirc.append("down")
              if right:
                 dirc.append("rightDown")
              if left:
                 dirc.append("leftDown")
           if event.key == pygame.K_a:
              left = True
              dirc.append("left")
              if up:
                 dirc.append("leftUp")
              if down:
                 dirc.append("leftDown")
              
           if event.key == pygame.K_d:
              right = True 
              dirc.append("right")
              if down:
                 dirc.append("rightDown")
              if up:
                 dirc.append("rightUp")

           if event.key == pygame.K_o and dash_allow and dash == False:
              if last_time - dash_cd >= 3:
                 dash = True  
                 dash_cd = time.time()

           if event.key == pygame.K_p:
              if last_time - shoot_cd >= .5:
                 bullets.append(make_bullet(p.rect))
                 shoot_cd = time.time()

           if event.key == pygame.K_SPACE and start == False:
              start = True
              start_time = pygame.time.get_ticks()
              astroid_cd = .01

        if event.type == pygame.KEYUP:
           if event.key == pygame.K_w:
              up = False
           if event.key == pygame.K_s:
              down = False
           if event.key == pygame.K_a:
              left = False
           if event.key == pygame.K_d:
              right = False    
    
    if start == False:
       start_text = 'Press Space to Start'
       my_big_font.render(display,start_text,(W // 4 - 140 // 2, 10))

    if start == True and last_time - astroid_cd >= 1 and len(astroids) < astroids_max:
      if random.randint(0,60) == 1: 
       if random.randint(0,60) >= 30:
          y =  random.randint(0,8) * 20
       else:   
          y = random.randint(6,13) * 20
       astroid_cd = time.time()
       astroids.append(obstacle(W // 2 + 10, y, 100))

    for astroid in astroids:
       astroid.damage(bullets, 50)
       remove = astroid.remove()
       if remove:
          astroids.remove(astroid)
       else:
          pygame.draw.rect(display, white, astroid.rect)
          astroid.rect.x -= 50 * dt   

    timer_text = list(str(current_time - start_time))
    timer_text.insert(-3, '.')
    timer_text.append('s')   
    my_big_font.render(display,timer_text,(10,10))

    for bullet in bullets:
       if bullet.x >= W // 2:
          bullets.remove(bullet)
       else:
         pygame.draw.rect(display, (255,0,0), bullet)
         bullet.x += 250 * dt

    display.blit(ss_img, (p.rect.x, p.rect.y))  

    WIN.blit(pygame.transform.scale(display,(W,H)),(0,0))
    pygame.display.update()