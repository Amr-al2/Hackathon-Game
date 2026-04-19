import pygame
import random
import os
import time
from player_class import player
from obstacles_class import obstacle
from enemies_class import enemy
from blaster_class import blast

pygame.init()

#Set Up Screen
W, H = 1200, 700
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

original_map = load_map("Map/spawn_map")
spawn_map = [row[:] for row in original_map]

#Data
high_score = 0
high_time = 0

f = open("data/high_scores.txt", "r")
high_score = f.readline().strip()
f.close()
if not high_score:
   high_score = "0"

f = open("data/best_time.txt", "r")
high_time = f.readline().strip()
f.close()
if not high_time:
   high_time = "0.0"

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

    def get_width(self, text):
     width = 0
     for char in text:
        if char != ' ':
            width += self.characters[char].get_width() + self.spacing
        else:
            width += self.space_width + self.spacing
     return width  

my_big_font = Font('Imgs/large_font.png')

#Text
score_text = ""
timer_text = ""
text = ""
end_text = ""

#Shoot
def make_bullet(rect):
    bullet = pygame.FRect(rect.right + 5, rect.bottom - rect.height // 2 - 2, 12, 4)
    return bullet

def make_eBullet(rect):
   bullet = pygame.FRect(rect.left + 5, rect.bottom - rect.height // 2 - 2, 12, 4)
   return bullet
#Rects

##Astroids
astroid_time = pygame.time.get_ticks()
sAstroid_time = pygame.time.get_ticks()
astroids_cd = 1
sAstroids_cd = 1.2
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
p = player(W // 4 - 25 // 2, H // 4 - 20 //2, 25, 20)
hearts = 5
total_score = 0
wave = 0
start_wave = False
iframes = False
iframes_cd = 0.0
blip = False
blips = 0

#Enemies
enemy_cd = pygame.time.get_ticks()
enemy_img = loadify("Imgs/enemy_ship.png")
enemies = []
max_enemies = 8

#Blaster
warning_img = loadify("Imgs/warning_sign.png")
max_blasters = 0

#Game Loop
clock = pygame.time.Clock()
run = True
while run:
    
    #Delta Time
    dt = clock.tick(FPS) / 1000
    last_time = time.time()

    display.fill(black) 
    
    num = 0
    display.fill(black)   

    #Time Tracker and Score Tracker
    if start == True:
      current_time = pygame.time.get_ticks()
      timer_text = list(str(current_time - start_time))
      timer_text.insert(-3, '.')
      timer_text.append('s')   
      my_big_font.render(display,timer_text,(5,H // 2 - 15))
      #Score
      my_big_font.render(display,str(total_score),(5, H // 2 - 35))
      #Wave Counter
      my_big_font.render(display,"Wave " + str(wave), (W // 4 - 20, H // 2 - 20))

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

           if event.key == pygame.K_s:
              down = True
   
           if event.key == pygame.K_a:
              left = True
              
           if event.key == pygame.K_d:
              right = True 

           if event.key == pygame.K_o and dash_allow and dash == False and start == True:
              if last_time - dash_cd >= 3:
               dash = True  
               iframes = True
               iframes_cd = time.time()
               dash_cd = time.time()

               if right and up:
                  dirc.append("rightUp")
               elif right and down:
                  dirc.append("rightDown")
               elif left and up:
                  dirc.append("leftUp")
               elif left and down:
                  dirc.append("leftDown")
               elif right:
                  dirc.append("right")
               elif left:
                  dirc.append("left")
               elif up:
                  dirc.append("up")
               elif down:
                  dirc.append("down")
               else:
                  dirc.append("right")

           if event.key == pygame.K_p and start == True:
              if last_time - shoot_cd >= .2:
                 bullets.append(make_bullet(p.rect))
                 shoot_cd = time.time()

           if event.key == pygame.K_SPACE and start == False:
              start = True
              end_text = ""
              vel = 150
              total_score = 0
              p.rect.x , p.rect.y = W // 4 - 25 // 2, H // 4 - 20 // 2
              start_time = pygame.time.get_ticks()
              enemy_cd = time.time()
              iframes_cd = time.time()
              wave = 1
              max_blasters = 0
              start_wave = True
              hearts = 5
              astroid_time = .01
              sAstroid_time = .01
              astroids_cd = 1
              sAstroids_cd = 1.2
               

        if event.type == pygame.KEYUP:
           if event.key == pygame.K_w:
              up = False
           if event.key == pygame.K_s:
              down = False
           if event.key == pygame.K_a:
              left = False
           if event.key == pygame.K_d:
              right = False    
   
    if iframes and last_time - iframes_cd >= .5:  
       iframes = False

    if iframes:
       blip = True   

    if blip and last_time - iframes_cd >= .075:
       blip = False

    if start == True and last_time - astroid_time >= astroids_cd:
      if random.randint(0,30) == 1: 
       if random.randint(0,60) >= 30:
          y =  random.randint(0,8) * 20
       else:   
          y = random.randint(6,13) * 20
       astroid_time = time.time()
       i = random.randint(0,4)
       astroids.append(obstacle(W // 2 + 10, y, 27, 27, 100, astroid_imgs[i]))

    if start == True and last_time - sAstroid_time >= sAstroids_cd:  
       if random.randint(0,30) == 1:
         x = random.randint(0,25) * 15 
         i = random.randint(0,4)
         if random.randint(0,60) >= 30:
            y = - 20
            sAstroids[0].append(obstacle(x, y, 15, 15, 50, sAstroid_imgs[i])) 
         else:
            y = H // 2 + 20
            sAstroids[1].append(obstacle(x, y, 15, 15, 50, sAstroid_imgs[i])) 
         sAstroid_time = time.time() 

    if last_time - enemy_cd >= 3 and start_wave:
       r = 0
       if wave >= 8:
        r = wave - 8
       for i in range(0, wave + 1):
          x = random.randint(0,10)
          y = random.randint(0,2)
          while spawn_map[x][y] == '1':
                x = random.randint(0,10)
                y = random.randint(0,2) 
          spawn_map[x][y] = '1'
          spacing = 10
          enemies.append(enemy((spacing * y + (y * 32) + (32 * 4 + spacing *  4)) + W // 2, x * 20 + spacing * x + 15, 32, 20, 150, enemy_img, spacing * y + (y * 32) + (W // 2 - (32 * 4 + spacing *  4))))
       start_wave = False  
   
    for e in enemies[:]:
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
        e.shoot(time.time(), make_eBullet(e.rect))

    for bullet in enemy.bullets[:]:
        if bullet.right <= 0:
           enemy.bullets.remove(bullet)
        elif bullet.colliderect(p.rect) and iframes == False: 
           hearts -= 1
           enemy.bullets.remove(bullet)
           iframes = True
           iframes_cd = time.time()
        else:
           pygame.draw.rect(display, white, bullet)
           bullet.x -= 150 * dt      

    for astroid in sAstroids[0][:]:
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

    for astroid in sAstroids[1][:]:
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

    for astroid in astroids[:]:
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
          display.blit(astroid.img, (astroid.rect.x, astroid.rect.y))
          astroid.rect.x -= 50 * dt   
       remove = False    

    if len(blast.blasts) < max_blasters and start:
          spacing = 10
          num = random.randint(0,9) 
          x = num * (50 // 2) + (spacing * num)
          blast.blasts.append(blast(x, -2000 // 2, 50 // 2, 2000 // 2, warning_img, last_time))

    for b in blast.blasts[:]:
       if b.warning_sign(last_time):
          display.blit(b.img, (b.rect.x,10))  
       else: 
           blast_remove = b.remove(H // 2) 
           if blast_remove:
              blast.blasts.remove(b)     
           elif b.rect.colliderect(p.rect) and iframes == False:
               hearts -= 1
               iframes = True
               iframes_cd = time.time() 
           else:
              pygame.draw.rect(display, white, b.rect)
              b.rect.y += blast.vel * dt    

    for x in range(0, hearts):
        display.blit(heart_img, ((W // 2) - (16 * (x + 1) + 5 * (x + 1)),10))  

    for bullet in bullets[:]:
       if bullet.x >= W // 2:
          bullets.remove(bullet)
       else:
         pygame.draw.rect(display, white, bullet)
         bullet.x += 250 * dt
    
    if start and start_wave == False:
       if len(enemies) <= 0:
        wave += 1
        spawn_map = [row[:] for row in original_map]
        start_wave = True
        astroids_cd -= .07
        sAstroids_cd -= .07
        if hearts < 5:
            hearts += 1

    if wave >= 3:
       max_blasters = 1

    if wave >= 5:    
       max_blasters = 2

    if wave >= 7:
       max_blasters = 3

    if wave >= 8:
       max_blasters = 4

    if wave > 10:
       wave = 10
       end_text = "YOU WIN!"   

    if start == True and hearts == 0:
       start = False 
       text = "Time Survived: "
       score_text = "Final Score: " + str(total_score)
       bullets.clear()
       enemy.bullets.clear()
       blast.blasts.clear()
       astroids.clear()
       sAstroids[0].clear()
       sAstroids[1].clear()
       enemies.clear()
       vel = 0
       if int(high_score) < total_score:
          high_score = str(total_score)
          f = open("data/high_scores.txt","w")
          f.write(high_score)
          f.close()
       if float(high_time) < (current_time - start_time) / 1000:
          high_time = "".join(timer_text).strip("s")
          f = open("data/best_time.txt","w")
          f.write(high_time)
          f.close()

    if hearts > 0 and blip == False:
       display.blit(ss_img, (p.rect.x, p.rect.y))  

    if start == False:
     center_x = W // 4  # since display is W//2 wide, center is W//4

     def render_centered(text, y):
        w = my_big_font.get_width(str(text))
        my_big_font.render(display, str(text), (center_x - w // 2, y))

     render_centered("Press Space to Start", 10)
     render_centered("Best Time: " + high_time + "s", 35)
     render_centered("Highest Score: " + high_score, 55)
     render_centered(text, H // 4 - 40)
     render_centered("".join(timer_text), H // 4 - 20)
     render_centered(score_text, H // 4)
     render_centered(end_text, H // 4 - 60)


    WIN.blit(pygame.transform.scale(display,(W,H)),(0,0))
    pygame.display.update()
