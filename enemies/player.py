import pygame
from items.ship import Ship
import os
import random
import config.config as config
from enemies.mystery_ship import MysteryShip


class Player(Ship):
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0, 0)
    gray = (128, 128, 128)
    random_score = {
        1: 150,
        2: 200,
        3: 300
    }

    def __init__(self, x, y, health=100, armor=100):
        super().__init__(x, y, health)
        self.ship_img = config.YELLOW_SPACE_SHIP
        self.score = 0
        self.laser_img = config.YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.armor = armor
        self.max_armor = armor
        self.lives = 3
        self.velocity = 5

    def move_lasers(self, vel, objs, bunkers):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.out_of_screen(config.HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= laser.power
                        if isinstance(obj, MysteryShip):
                            if obj.health >= 700:
                                self.score += self.random_score[random.randint(1, 3)]
                            else:
                                self.score += 300
                        if obj.health <= 0:
                            self.score += 100
                        self.lasers.remove(laser)
            for b in bunkers:
                if laser.collision(b):
                    self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)
        self.armor_bar(window)

    def health_bar(self, window):
        red_rect, green_rect = self.get_rectangles(10, self.health, self.max_health)
        pygame.draw.rect(window, self.red, red_rect)
        pygame.draw.rect(window, self.green, green_rect)

    def armor_bar(self, window):
        black_rect, gray_rect = self.get_rectangles(20, self.armor, self.max_armor)
        pygame.draw.rect(window, self.black, black_rect)
        pygame.draw.rect(window, self.gray, gray_rect)

    def get_rectangles(self, dy, capacity, max_capacity):
        rect_1 = (self.x, self.y + self.ship_img.get_height() + dy, self.ship_img.get_width(), 10)
        rect_2 = (self.x, self.y + self.ship_img.get_height() + dy,
                  self.ship_img.get_width() * (capacity / max_capacity), 10)
        return rect_1, rect_2
