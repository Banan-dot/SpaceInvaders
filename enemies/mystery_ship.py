from items.ship import Ship
import pygame
import random
from items.laser import Laser
from config.config import COLOR_MAP


class MysteryShip(Ship):
    def __init__(self, x, y, health=3000):
        super().__init__(x, y, health)
        self.color = "mystery"
        self.ship_img, self.laser_img = COLOR_MAP[self.color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.velocity = 3
        self.to_x = random.randint(100, 600)
        self.to_y = random.randint(100, 250)

    def move(self, vel):
        dy = abs(self.y - self.to_y)
        dx = abs(self.x - self.to_x)
        if dy >= 3 and dx >= 3:
            if dy:
                self.y -= vel * self.sign(self.y - self.to_y)
            if dx:
                self.x -= vel * self.sign(self.x - self.to_x)
        else:
            self.to_x = random.randint(50, 700)
            self.to_y = random.randint(30, 250)

    def shoot(self):
        if self.cool_down_counter == 0:
            left = pygame.transform.rotate(self.laser_img, 30)
            right = pygame.transform.rotate(self.laser_img, -30)
            laser_left = Laser(self.x, self.y, left, -1 / 2, -1 / 2, power=50)
            laser_straight = Laser(self.x, self.y, self.laser_img, 0, -1, power=50)
            laser_right = Laser(self.x, self.y, right, 1 / 2, -1 / 2, power=50)
            self.lasers.append(laser_left)
            self.lasers.append(laser_straight)
            self.lasers.append(laser_right)
            self.cool_down_counter = 1

    @staticmethod
    def sign(x):
        return 0 if x == 0 else 1 if x > 0 else -1
