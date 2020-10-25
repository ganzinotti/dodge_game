import pygame as pg
from typing import Tuple

vec = pg.math.Vector2


class Enemy(pg.sprite.Sprite):
    def __init__(
        self, size: int, color: Tuple[int, int, int], position: tuple, velocity: tuple
    ):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=position)

        self.size = size
        self.color = color
        self.pos = vec(*position)
        self.vel = vec(*velocity)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
