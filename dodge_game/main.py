import pygame as pg
from settings import (
    WIDTH,
    HEIGHT,
    TITLE,
    FPS,
    BLACK,
    WHITE,
    BLUE,
    RED,
    YELLOW,
    PLAYER_RADIUS,
    PLAYER_FRICTION,
    PLAYER_ACC,
    FONT_NAME,
    BORDER,
    BOTTOM_PADDING,
)
import random
import math
from enemy import Enemy
from player import Player
from buffs import Buff
from typing import Union


class Game:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        # pg.mixer.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # start a new game
        self.score = 0
        self.level = 0
        self.buff_correction = 0
        self.speed_lb = 2
        self.speed_ub = 6

        self.all_enemies = pg.sprite.Group()

        self.all_buffs = pg.sprite.Group()
        self.add_buff()

        self.all_players = pg.sprite.Group()
        self.player = Player(PLAYER_RADIUS, PLAYER_FRICTION, PLAYER_ACC, RED)
        self.all_players.add(self.player)

        self.run()

    def add_buff(self):
        pos_x = random.randint(0 + 15 * BORDER, WIDTH - 15 * BORDER)
        pos_y = random.randint(0 + 1 * BORDER, HEIGHT - 3 * BORDER)
        buff = Buff(15, (pos_x, pos_y))
        self.all_buffs.add(buff)

    def run(self):
        # Game Loop
        self.playing = True

        while self.playing:
            self.clock.tick(FPS)
            self.events()

            if random.random() < 0.1:
                enemy = self.add_enemy_to_board()
                self.all_enemies.add(enemy)

            self.update()
            self.update_score()

            self.collected_buff()
            collision = self.check_collision_all_enemies()
            if collision:
                self.playing = False

            self.draw()

    def add_enemy_to_board(self):
        size = random.randint(7, 13)
        height = random.randint(0, HEIGHT - BOTTOM_PADDING)

        self.level = self.score // 50
        base_speed = (
            random.randint(self.speed_lb, self.speed_ub)
            + self.level
            - self.buff_correction
        )
        if random.random() < 0.9:
            # enemy from right
            return Enemy(
                size,
                BLUE,
                (WIDTH, height),
                (-1 * base_speed, 0),
            )
        else:
            # enemy from left
            return Enemy(
                size,
                YELLOW,
                (1, height),
                (base_speed, 0),
            )

    def update_score(self):
        for enemy in self.all_enemies:
            if (enemy.pos.x > WIDTH) or (enemy.pos.x < 0):
                enemy.kill()
                self.score += 1
            if 0 < enemy.pos.y > HEIGHT:
                enemy.kill()
                self.score += 1

    def update(self):
        self.all_players.update()
        self.all_enemies.update()
        self.all_buffs.update()

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(BLACK)

        self.all_enemies.draw(self.screen)
        self.all_players.draw(self.screen)
        self.all_buffs.draw(self.screen)

        pg.draw.line(
            self.screen,
            WHITE,
            (0, HEIGHT - BOTTOM_PADDING),
            (WIDTH, HEIGHT - BOTTOM_PADDING),
        )

        pg.draw.rect(
            self.screen, RED, (0, WIDTH - BOTTOM_PADDING, WIDTH, BOTTOM_PADDING)
        )

        net_speed = round(
            (self.speed_lb + self.speed_ub) / 2 + self.level - self.buff_correction, 2
        )
        self.draw_text(
            f"Level: {self.level + 1}, Speed: {net_speed}",
            size=18,
            color=WHITE,
            x=BORDER,
            y=HEIGHT - BORDER,
            alignment="midleft",
        )

        self.draw_text(
            f"Score: {self.score}",
            size=18,
            color=WHITE,
            x=WIDTH - BORDER,
            y=HEIGHT - BORDER,
            alignment="midright",
        )
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.ogg'))
        # pg.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        self.draw_text(TITLE, size=48, color=WHITE, x=WIDTH / 2, y=HEIGHT / 4)
        self.draw_text(
            "Arrows to move, Don't get hit!",
            size=22,
            color=WHITE,
            x=WIDTH / 2,
            y=HEIGHT / 2,
        )
        self.draw_text(
            "Press a key to play", size=22, color=WHITE, x=WIDTH / 2, y=HEIGHT * 3 / 4
        )
        # self.draw_text(f"High Score: {}" + str(self.highscore), size=22, color=WHITE, x=WIDTH / 2, y=15)
        pg.display.flip()
        self.wait_for_key()
        # pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, *, size, color, x, y, alignment: str = "midtop"):
        font = pg.font.SysFont(FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if alignment == "midtop":
            text_rect.midtop = (x, y)
        elif alignment == "midright":
            text_rect.midright = (x, y)
        else:
            text_rect.midleft = (x, y)

        self.screen.blit(text_surface, text_rect)

    def show_go_screen(self):
        if not self.running:
            return None

        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", size=48, color=WHITE, x=WIDTH / 2, y=HEIGHT / 4)
        self.draw_text(
            f"Score: {self.score}", size=22, color=WHITE, x=WIDTH / 2, y=HEIGHT / 2
        )
        self.draw_text(
            "Press a key to play again",
            size=22,
            color=WHITE,
            x=WIDTH / 2,
            y=HEIGHT * 3 / 4,
        )

        # if self.score > self.highscore:
        #     self.highscore = self.score
        #     self.draw_text("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        #     with open(path.join(self.dir, HS_FILE), 'w') as f:
        #         f.write(str(self.score))
        # else:
        #     self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()

    def collected_buff(self):
        for buff in self.all_buffs:
            if self._check_collision_single_object(self.player, buff):
                buff.kill()
                self.add_buff()
                self.buff_correction += 0.2

    def check_collision_all_enemies(self) -> bool:
        for enemy in self.all_enemies:
            if self._check_collision_single_object(self.player, enemy):
                return True

        return False

    @staticmethod
    def _check_collision_single_object(player: Player, obj: Union[Enemy, Buff]) -> bool:
        center_distance = math.sqrt(
            (player.pos.x - obj.pos.x) ** 2 + (player.pos.y - obj.pos.y) ** 2
        )

        if center_distance < (player.radius + obj.size / 2):
            return True
        else:
            return False


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
