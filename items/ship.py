from items.laser import Laser
from config.config import HEIGHT
import pygame
from gui.sound import Sound


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.sound = Sound.shoot
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj, bunkers):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.out_of_screen(HEIGHT):
                self.lasers.remove(laser)
            if laser.collision(obj):
                self.reduce_health(obj)
                self.lasers.remove(laser)
            for bunker in bunkers:
                if laser.collision(bunker):
                    bunker.health -= 50
                    self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            self.sound.play()
            left = pygame.transform.rotate(self.laser_img, 30)
            right = pygame.transform.rotate(self.laser_img, -30)
            laser_left = Laser(self.x, self.y, left, -1 / 2, -1 / 2)
            laser_straight = Laser(self.x, self.y, self.laser_img, 0, -1)
            laser_right = Laser(self.x, self.y, right, 1 / 2, -1 / 2)
            self.lasers.append(laser_left)
            self.lasers.append(laser_straight)
            self.lasers.append(laser_right)
            self.cool_down_counter = 1

    def overpower_shoot(self):
        if self.cool_down_counter == 0:
            self.sound.play()
            laser_straight = Laser(self.x, self.y, self.laser_img, 0, -1, power=300)
            self.lasers.append(laser_straight)
            self.cool_down_counter = 0.5

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    @staticmethod
    def reduce_health(obj):
        if obj.armor >= 10:
            obj.armor -= 10
        elif 0 < obj.armor < 10:
            temp = 10 - obj.armor
            obj.armor = 0
            obj.health -= temp
        else:
            obj.health -= 10
