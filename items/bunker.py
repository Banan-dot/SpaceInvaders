from pygame import mask


class Bunker:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.health = 500
        self.img = img
        self.mask = mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
