import pygame
import random

class enemy:

    def __init__(self, x, y, w, h, hp, img, spawn_map):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = hp
        self.img = img 
        self.rect = pygame.FRect(x, y, w, h)
        
    def spawn(self, spawn_map):
        done = False
        y = 0
        for row in spawn_map:
              x = 0
              for num in row:  
                 if num == '1':
                    self.rect = pygame.FRect(x * self.w, y * self.h, self.w, self.h) 
                    print(self.rect)
                    self.destination = 16 * x + (500 - (16 * 4))
                    break
                 x += 1
              y += 1
              
        