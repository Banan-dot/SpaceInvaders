import pygame
import math


class Laser:
    velocity = 5

    def __init__(self, x, y, img, k_x, k_y, *, power=100):
        self.x = x
        self.y = y
        self.k_x = k_x
        self.k_y = k_y
        self.power = power
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.x = int(self.x - self.k_x * vel)
        self.y = int(self.y - self.k_y * vel)

    def out_of_screen(self, height):
        return not (height >= self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
