import pygame
import math

class obstacle:
    w = 25
    h = 25

    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.rect = pygame.FRect(x, y, obstacle.w, obstacle.h)

    def damage(self, bullets, damage):
      for bullet in bullets: 
       if self.rect.colliderect(bullet):
          self.hp -= damage 
          bullets.remove(bullet) 
           
    def remove(self):
        if self.x <= 0 or self.hp == 0:
           return True
        else: return False