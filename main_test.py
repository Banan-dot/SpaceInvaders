#!/usr/bin/env python3

import sys
import unittest
import pygame
from states.states import Save
from items.bunker import Bunker
from enemies.space_invader_red import SpaceInvaderRed
from enemies.space_invader_blue import SpaceInvaderBlue
from enemies.space_invader_green import SpaceInvaderGreen
from items.laser import Laser
from enemies.player import Player
from items.ship import Ship
from config.config import COLOR_MAP
from enemies.mystery_ship import MysteryShip


class TestPlayer(unittest.TestCase):
    def test_initialization(self):
        player = Player(10, 20)
        self.assertEqual(10, player.x)
        self.assertEqual(20, player.y)
        self.assertEqual(100, player.max_health)
        self.assertEqual(0, player.score)


class TestLaser(unittest.TestCase):
    def test_initialization(self):
        laser = Laser(10, 20, pygame.image.load("./assets/pixel_laser_yellow.png"), 0, 0)
        self.assertEqual(10, laser.x)
        self.assertEqual(20, laser.y)

    def test_move(self):
        laser = Laser(10, 20, pygame.image.load("./assets/pixel_laser_yellow.png"), 0, 0)
        laser.move(20)
        self.assertEqual(20, laser.y)

    def test_out_of_screen(self):
        laser = Laser(10, 20, pygame.image.load("./assets/pixel_laser_yellow.png"), 0, 0)
        self.assertFalse(laser.out_of_screen(100))
        self.assertTrue(laser.out_of_screen(10))
        self.assertTrue(laser.out_of_screen(-10))
        self.assertFalse(laser.out_of_screen(20))

    def test_collision(self):
        laser = Laser(10, 20, pygame.image.load("./assets/pixel_laser_yellow.png"), 0, 0)
        player = Player(5, 10)
        self.assertTrue(laser.collision(player))

    def test_not_collision(self):
        laser = Laser(100, 200, pygame.image.load("./assets/pixel_laser_yellow.png"), 0, 0)
        player = Player(0, 0)
        self.assertFalse(laser.collision(player))


class TestShip(unittest.TestCase):
    def test_initialization(self):
        ship = Ship(10, 20)
        self.assertEqual(10, ship.x)
        self.assertEqual(20, ship.y)
        self.assertEqual(100, ship.health)
        self.assertEqual(0, ship.cool_down_counter)
        self.assertEqual(30, ship.COOLDOWN)

    def test_cooldown_0(self):
        ship = Ship(10, 20)
        ship.cooldown()
        self.assertEqual(0, ship.cool_down_counter)

    def test_cooldown_1(self):
        ship = Ship(10, 20)
        ship.cool_down_counter = 1
        ship.cooldown()
        self.assertEqual(2, ship.cool_down_counter)

    def test_cooldown_35(self):
        ship = Ship(10, 20)
        ship.cool_down_counter = 35
        ship.cooldown()
        self.assertEqual(0, ship.cool_down_counter)

    def test_shooting(self):
        ship = Ship(10, 20)
        ship.laser_img = pygame.image.load("./assets/pixel_laser_yellow.png")
        ship.shoot()
        self.assertEqual(1, ship.cool_down_counter)

    def test_get_width(self):
        ship = Ship(10, 20)
        ship.ship_img = pygame.image.load("./assets/pixel_ship_yellow.png")
        self.assertEqual(100, ship.get_width())

    def test_get_height(self):
        ship = Ship(10, 20)
        ship.ship_img = pygame.image.load("./assets/pixel_ship_yellow.png")
        self.assertEqual(90, ship.get_height())


class TestEnemy(unittest.TestCase):
    def test_initialization(self):
        enemy = SpaceInvaderRed(10, 20)
        self.assertEqual(10, enemy.x)
        self.assertEqual(20, enemy.y)
        self.assertEqual(300, enemy.health)
        self.assertEqual([], enemy.lasers)
        self.assertEqual(0, enemy.cool_down_counter)

    def test_move(self):
        enemy = SpaceInvaderRed(10, 20)
        enemy.move(20)
        self.assertEqual(40, enemy.y)

    def test_shoot(self):
        enemy = SpaceInvaderRed(20, 30)
        enemy.shoot()
        self.assertEqual(0, enemy.lasers[0].x)
        self.assertEqual(30, enemy.lasers[0].y)
        self.assertEqual(1, enemy.cool_down_counter)


class TestUFO(unittest.TestCase):
    def test_initialization(self):
        enemy = MysteryShip(10, 20)
        self.assertEqual(10, enemy.x)
        self.assertEqual(20, enemy.y)
        self.assertEqual(3000, enemy.health)
        self.assertEqual([], enemy.lasers)
        self.assertEqual(0, enemy.cool_down_counter)

    def test_move(self):
        enemy = MysteryShip(10, 20)
        enemy.move(20)
        self.assertEqual(40, enemy.y)

    def test_shoot(self):
        enemy = MysteryShip(20, 30)
        enemy.shoot()
        self.assertEqual(20, enemy.lasers[0].x)
        self.assertEqual(30, enemy.lasers[0].y)
        self.assertEqual(20, enemy.lasers[1].x)
        self.assertEqual(30, enemy.lasers[1].y)
        self.assertEqual(20, enemy.lasers[2].x)
        self.assertEqual(30, enemy.lasers[2].y)
        self.assertEqual(1, enemy.cool_down_counter)

    def test_sign(self):
        enemy = MysteryShip(10, 20)
        self.assertEqual(0, enemy.sign(0))
        self.assertEqual(1, enemy.sign(1))
        self.assertEqual(-1, enemy.sign(-2))


class TestBunker(unittest.TestCase):
    def test_initialization(self):
        bunker = Bunker(10, 20, pygame.image.load("./assets/icon.png"))
        self.assertEqual(10, bunker.x)
        self.assertEqual(20, bunker.y)
        self.assertEqual(pygame.image.load("./assets/icon.png").get_size(), bunker.img.get_size())


class TestStates(unittest.TestCase):
    def test_load(self):
        file = Save('./test_states/data')
        file.add("Daniil Semke", 10000)
        answer = file.get("Daniil Semke")
        self.assertEqual(10000, answer)

    def test_save_state(self):
        file = Save('./test_states/data')
        try:
            file.add("my_file", 1010)
        except Exception as e:
            raise e

    def test_get_tuple(self):
        file = Save('./test_states/data')
        result = file.get_tuple()
        expected_res = [('Bay', 1), ('Daniil Semke', 10000), ('my_file', 1010), ('my_self.file', 1010)]
        self.assertEqual(expected_res, result)

    def test_get_state(self):
        file = Save('./test_states/data')
        file.add("Bay", 1)
        self.assertEqual(1, file.get("Bay"))

    def test_get_state_without_key(self):
        file = Save('./test_states/data')
        self.assertEqual(0, file.get("Vladimir Putin"))

    def test_get_keys(self):
        file = Save('./test_states/data')
        keys = file.get_keys()
        self.assertEqual(['Bay', 'Daniil Semke', 'my_file', "my_self.file"], keys)

    def test_get_items(self):
        file = Save('./test_states/data')
        items = list(file.get_items())
        self.assertEqual([('Bay', 1),
                          ('Daniil Semke', 10000),
                          ('my_file', 1010),
                          ('my_self.file', 1010)], items)

    def test_get_values(self):
        file = Save('./test_states/data')
        val = file.get_values()
        self.assertEqual([1, 10000, 1010, 1010], val)


if __name__ == '__main__':
    unittest.main()
