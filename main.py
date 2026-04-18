import pygame
import math
import random
import os
import time
from player_class import player
from obstacles_class import obstacle
from enemies_class import enemy
pygame.init()

#Set Up Screen
W, H = 1000, 700
WIN = pygame.display.set_mode((W, H))
display = pygame.Surface((W // 2, H // 2))
pygame.display.set_caption("Hackathon")
pygame.mouse.set_visible(True)

#FPS
FPS = 60

#Varibles
last_time = time.time()

start = False
current_time = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()
timer_text = str("0.0s")

##Shoot
shoot_cd = 1
bullets = []

#Movement
up = False
down = False
left = False
right = False
vel = 0

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

ss_img = loadify("Imgs/space_ship.png")
heart_img = loadify("Imgs/Heart.png")

#Map Render
def load_map(path):
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

spawn_map = load_map("Map/spawn_map")


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

my_big_font = Font('Imgs/large_font.png')

#Shoot
def make_bullet(rect):
    bullet = pygame.FRect(rect.right + 5, rect.bottom - rect.height // 2 - 2, 12, 4)
    return bullet

#Rects

##Astroids
astroid_cd = pygame.time.get_ticks()
sAstroid_cd = pygame.time.get_ticks()
astroidRect = pygame.FRect(W // 2 + 10, 0, 25, 25)
sAstroidRect = pygame.FRect(0, 0, 15, 15)
astroids = []
sAstroids = []
topAstroids = []
bottomAstroids = []
sAstroids.append(topAstroids)
sAstroids.append(bottomAstroids)

astroid_imgs = []
for i in range(1,6):
   astroid_imgs.append(loadify("big_astroids/big_astroid" + str(i) + ".png"))
sAstroid_imgs = []
for i in range(1,6):
   sAstroid_imgs.append(loadify("small_astroids/small_astroid" + str(i) + ".png"))

##Borders
tiles = [pygame.Rect(0, 0 - 50, W // 2, 50), pygame.Rect(0 - 50, 0, 50, H // 2), pygame.Rect(0, H // 2, W // 2, 50), pygame.Rect(W // 2, 0, 50, H // 2)]

##BG
bg_imgs = []
bg_imgs.append(loadify("Imgs/bg_1.png"))
bg_imgs.append(loadify("Imgs/bg_2.png"))
bg_imgs.append(loadify("Imgs/bg_1.png"))
bgs = [pygame.FRect(0, 0, W // 2, H // 2), pygame.FRect(W // 2, 0, W // 2, H // 2), pygame.FRect(W, 0, W // 2, H // 2)]

bg_blocker = pygame.Rect(-W // 2 - 100 // 2, 0, 100 // 2, H // 2)

#Player
p = player(W // 4, H // 4, 32, 20)
hearts = 5
total_score = 0
wave = 0
start_wave = False
iframes = False
iframes_cd = 0.0

#Enemies
enemy_cd = pygame.time.get_ticks()
enemy_img = loadify("Imgs/enemy_ship.png")
enemies = []

#Game Loop
clock = pygame.time.Clock()
run = True
while run:

    #Delta Time
    dt = clock.tick(FPS) / 1000
    last_time = time.time()

    display.fill(black) 
    
    num = 0
    for bg in bgs:
      if bg.colliderect(bg_blocker):
       bg.x = W 
      display.blit(bg_imgs[num], (bg.x, 0))
      if start == True: 
       bg.x -= 140 * dt
       num += 1
    display.fill(black)   

    #Score
    my_big_font.render(display,str(total_score),(5, H // 2 - 30))

    #Time Tracker
    if start == True:
      current_time = pygame.time.get_ticks()
      timer_text = list(str(current_time - start_time))
      timer_text.insert(-3, '.')
      timer_text.append('s')   
    my_big_font.render(display,timer_text,(5,H // 2 - 15))

    movement = [0,0]

    if up:
       movement[1] -= vel * dt
    if down: 
       movement[1] += vel * dt
    if right:
       movement[0] += vel * dt
    if left:
       movement[0] -= vel * dt 

    if dash_count + 1 >= 4:
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

           if event.key == pygame.K_o and dash_allow and dash == False and start == True:
              if last_time - dash_cd >= 2:
                 dash = True  
                 dash_cd = time.time()

           if event.key == pygame.K_p and start == True:
              if last_time - shoot_cd >= .3:
                 bullets.append(make_bullet(p.rect))
                 shoot_cd = time.time()

           if event.key == pygame.K_SPACE and start == False:
              start = True
              vel = 150
              total_score = 0
              p.rect.x , p.rect.y = W // 4, H // 4
              start_time = pygame.time.get_ticks()
              enemy_cd = time.time()
              iframes_cd = time.time()
              wave = 1
              start_wave = True
              hearts = 5
              astroid_cd = .01
              sAstroid_cd = .01

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
   
    if iframes and last_time - iframes_cd >= 1:  
       iframes = False

    if start == True and last_time - astroid_cd >= 1:
      if random.randint(0,30) == 1: 
       if random.randint(0,60) >= 30:
          y =  random.randint(0,8) * 20
       else:   
          y = random.randint(6,13) * 20
       astroid_cd = time.time()
       i = random.randint(0,4)
       astroids.append(obstacle(W // 2 + 10, y, 27, 27, 100, astroid_imgs[i]))

    if start == True and last_time - sAstroid_cd >= 1.2:  
       if random.randint(0,30) == 1:
         x = random.randint(0,16) * 15 
         i = random.randint(0,4)
         if random.randint(0,60) >= 30:
            y = - 20
            sAstroids[0].append(obstacle(x, y, 15, 15, 50, sAstroid_imgs[i])) 
         else:
            y = H // 2 + 20
            sAstroids[1].append(obstacle(x, y, 15, 15, 50, sAstroid_imgs[i])) 
         sAstroid_cd = time.time() 

    if last_time - enemy_cd >= 3 and start_wave:
       for i in range(0, wave + 1):
          x = random.randint(0,10)
          y = random.randint(0,3)
          if spawn_map[x][y] == '1':
             while spawn_map[x][y] == '1':
                x = random.randint(0,10)
                y = random.randint(0,3) 
                spawn_map[x][y] == '1'
          spawn_map[x][y] = '1'
          spacing = 10
          e = enemy((spacing * y + (y * 32) + (32 * 4 + spacing *  4)) + W // 2, x * 20 + spacing * x + 15, 32, 20, 150, enemy_img, spacing * y + (y * 32) + (W // 2 - (32 * 4 + spacing *  4)))
          enemies.append(e)
       start_wave = False  

    if len(enemies) >= 0:
     for e in enemies:
       e.damage(bullets, 50)
       remove, points = e.remove()
       total_score += points
       if e.rect.colliderect(p.rect) and iframes == False:
          hearts -= 1
          iframes = True
          iframes_cd = time.time()
       if remove:
          enemies.remove(e)
       else:   
        display.blit(e.img, (e.rect.x, e.rect.y))
        e.move(50 * dt)

    for astroid in sAstroids[0]:
       astroid.damage(bullets, 50)
       remove, points = astroid.remove()
       total_score += points
       if remove:
          sAstroids[0].remove(astroid)
       elif astroid.rect.colliderect(p.rect) and iframes == False:
          hearts -= 1
          iframes = True
          iframes_cd = time.time()
          sAstroids[0].remove(astroid)   
       else:
          display.blit(astroid.img,(astroid.rect.x, astroid.rect.y))
          astroid.rect.y += 50 * dt
       remove = False  

    for astroid in sAstroids[1]:
       astroid.damage(bullets, 50)
       remove, points = astroid.remove()
       total_score += points
       if remove:
          sAstroids[1].remove(astroid)
       elif astroid.rect.colliderect(p.rect) and iframes == False:
          hearts -= 1
          iframes = True
          iframes_cd = time.time()
          sAstroids[1].remove(astroid)   
       else:
          display.blit(astroid.img,(astroid.rect.x, astroid.rect.y))
          astroid.rect.y -= 50 * dt   
       remove = False    

    for astroid in astroids:
       astroid.damage(bullets, 50)
       remove, points = astroid.remove()
       total_score += points
       if remove:
          astroids.remove(astroid)
       elif astroid.rect.colliderect(p.rect) and iframes == False:
          hearts -= 1
          iframes = True
          iframes_cd = time.time()
          astroids.remove(astroid)   
       else:
          i = random.randint(0,4)
          display.blit(astroid.img, (astroid.rect.x, astroid.rect.y))
          astroid.rect.x -= 50 * dt   
       remove = False    
     
    for x in range(0, hearts):
        display.blit(heart_img, (5 + (16 * x + 5 * x),10))  

    for bullet in bullets:
       if bullet.x >= W // 2:
          bullets.remove(bullet)
       else:
         pygame.draw.rect(display, white, bullet)
         bullet.x += 250 * dt

    if start == True and hearts == 0:
       start = False  
       astroids.clear()
       sAstroids[0].clear()
       sAstroids[1].clear()
       enemies.clear()
       vel = 0

    display.blit(ss_img, (p.rect.x, p.rect.y))  

    WIN.blit(pygame.transform.scale(display,(W,H)),(0,0))
    pygame.display.update()