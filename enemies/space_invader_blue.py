from items.ship import Ship
import pygame
from items.laser import Laser
from config.config import COLOR_MAP


class SpaceInvaderBlue(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.color = "blue"
        self.ship_img, self.laser_img = COLOR_MAP[self.color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.velocity = 2

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img, 0, -1)
            self.lasers.append(laser)
            self.cool_down_counter = 1
