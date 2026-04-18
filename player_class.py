import pygame

class player:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.FRect(x, y, w, h)

    def collision_test(self, rect, tiles: list):
        collisions = []
        for tile in tiles:
            if rect.colliderect(tile):
               collisions.append(tile)
        return collisions

    def move(self, rect, movement: list, tiles: list):
        rect.x += movement[0]
        collisions = self.collision_test(rect, tiles)
        for tile in collisions:
            if movement[0] > 0:
               rect.right = tile.left
            elif movement[0] < 0:
                rect.left = tile.right
        rect.y += movement[1]
        collisions = self.collision_test(rect, tiles)
        for tile in collisions:
            if movement[1] > 0:
               rect.bottom = tile.top
            elif movement[1] < 0:
                rect.top = tile.bottom 
        return rect     
                 
