import pygame as pg
from settings import GREEN

vec = pg.math.Vector2


class Buff(pg.sprite.Sprite):
    def __init__(self, size: int, position: tuple):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((size, size))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=position)

        self.size = size
        self.pos = vec(*position)

    def update(self):
        self.rect.center = self.pos
