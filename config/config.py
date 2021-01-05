import pygame
WIDTH, HEIGHT = 750, 750
YELLOW_SPACE_SHIP = pygame.image.load("./assets/pixel_ship_yellow.png")
YELLOW_LASER = pygame.image.load("./assets/pixel_laser_yellow.png")
RED_LASER = pygame.image.load("./assets/pixel_laser_red.png")
GREEN_LASER = pygame.image.load("./assets/pixel_laser_green.png")
BLUE_LASER = pygame.image.load("./assets/pixel_laser_blue.png")
RED_SPACE_SHIP = pygame.image.load("./assets/pixel_ship_red_small.png")
UFO_SHIP = pygame.image.load("./assets/ufo2.png")
GREEN_SPACE_SHIP = pygame.image.load("./assets/pixel_ship_green_small.png")
BLUE_SPACE_SHIP = pygame.image.load("./assets/pixel_ship_blue_small.png")
BUNKER = pygame.image.load("./assets/bunker.png")
BUNKER2 = pygame.image.load("./assets/bunker2.png")
GARAGE = pygame.image.load("./assets/Garage.png")
ICON = pygame.image.load("./assets/icon.png")
COLOR_MAP = {
    "mystery": (UFO_SHIP, RED_LASER),
    "red": (RED_SPACE_SHIP, RED_LASER),
    "green": (GREEN_SPACE_SHIP, GREEN_LASER),
    "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
}
