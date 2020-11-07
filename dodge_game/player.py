import pygame as pg
from settings import WIDTH, HEIGHT, PLAYER_RADIUS, RED, BOTTOM_PADDING
import pygame.gfxdraw as gfxdraw
from typing import Tuple

vec = pg.math.Vector2

PLAYER_IMG = pg.Surface((PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pg.SRCALPHA)
gfxdraw.aacircle(PLAYER_IMG, PLAYER_RADIUS, PLAYER_RADIUS, PLAYER_RADIUS - 1, RED)
gfxdraw.filled_circle(PLAYER_IMG, PLAYER_RADIUS, PLAYER_RADIUS, PLAYER_RADIUS - 1, RED)


class Player(pg.sprite.Sprite):
    def __init__(
        self, radius: int, friction: float, base_acc: float, color: Tuple[int, int, int]
    ):
        pg.sprite.Sprite.__init__(self)

        self.radius = radius
        self.friction = friction
        self.base_acc = base_acc
        self.color = color

        self.image = PLAYER_IMG

        center = (WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center=center)

        self.pos = vec(*center)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.acc.y = -self.base_acc
        if keys[pg.K_DOWN]:
            self.acc.y = self.base_acc
        if keys[pg.K_LEFT]:
            self.acc.x = -self.base_acc
        if keys[pg.K_RIGHT]:
            self.acc.x = self.base_acc

        # apply friction
        self.acc += self.vel * self.friction

        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT - BOTTOM_PADDING:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT - BOTTOM_PADDING

        self.rect.center = self.pos
