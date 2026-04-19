import pygame
import random
import time

class enemy:
    bullets = []
    def __init__(self, x, y, w, h, hp, img, destination):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = hp
        self.img = img 
        self.dest = destination
        self.shot_cd = 0
        self.sec = random.random()
        self.rect = pygame.FRect(x, y, w, h)

    def move(self, vel):
        if self.rect.x >= self.dest:  
           self.rect.x -= vel    

    def shoot(self, current_time, bullet_rect):
        if self.rect.x <= self.dest:
           if current_time - self.shot_cd >= self.sec + 0.6:
              enemy.bullets.append(bullet_rect) 
              self.shot_cd = time.time()

    def damage(self, bullets, damage):
      for bullet in bullets[:]: 
       if self.rect.colliderect(bullet):
          self.hp -= damage 
          bullets.remove(bullet)      

    def remove(self):
        if self.hp <= 0:
           return True, 100
        else: return False, 0    
              
        