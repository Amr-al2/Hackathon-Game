import pygame
import math

class obstacle:

    def __init__(self, x, y, w, h, hp, img):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = hp
        self.img = img
        self.rect = pygame.FRect(x, y, w, h)

    def damage(self, bullets, damage):
      for bullet in bullets: 
       if self.rect.colliderect(bullet):
          self.hp -= damage 
          bullets.remove(bullet) 
           
    def remove(self):
        if self.x <= 0:
           return True, 0
        elif self.hp == 0:
           return True, 10
        else: return False, 0