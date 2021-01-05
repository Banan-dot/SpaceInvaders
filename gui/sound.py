import pygame


class Sound:
    pygame.init()

    explosion = pygame.mixer.Sound('./music/explosion/explosion.wav')
    fastinvader1 = pygame.mixer.Sound('./music/fastinvader1/fastinvader1.wav')
    fastinvader4 = pygame.mixer.Sound('./music/fastinvader4/fastinvader4.wav')
    spaceinvaders1 = pygame.mixer.Sound('./music/spaceinvaders1/spaceinvaders1.wav')
    shoot = pygame.mixer.Sound('./music/shoot/shoot.wav')
    invaderkilled = pygame.mixer.Sound('./music/invaderkilled/invaderkilled.wav')
    ufo_highpitch = pygame.mixer.Sound('./music/ufo_highpitch/ufo_highpitch.wav')
    ufo_lowpitch = pygame.mixer.Sound('./music/ufo_lowpitch/ufo_lowpitch.wav')


