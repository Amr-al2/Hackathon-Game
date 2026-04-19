import pygame
import random
import time

class blast:

    blasts = []
    warning_timer = 3
    vel = 300

    def __init__(self, x, y, w, h, img, t):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.FRect(self.x, self.y, self.w, self.h)
        self.warning = True
        self.timer = t
        self.img = img

    def remove(self, limit):
        if self.rect.top >= limit:
           return True
        else:
           return False    

    def warning_sign(self, current_time):
        if current_time - self.timer >= blast.warning_timer:
           return False
        else:
           return True

