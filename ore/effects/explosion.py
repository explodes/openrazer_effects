#!/usr/bin/env python3.6
import math
import random

from ore.core.program import KeyboardProgram
from ore.core.utils import ROWS, COLS
from ore.registry.registry import register_effect


def deg_to_rad(theta):
    return theta * math.pi / 180


class Explosion(object):
    def __init__(self, center=(ROWS // 2, COLS // 2), radius=0, color=(255, 75, 0), resolution=20):
        self.center = center
        self.radius = radius
        self.resolution = resolution
        self.color = color

    def expand(self, delta=0.45):
        self.radius += delta

    def write_to(self, matrix):
        delta = 360 / self.resolution
        row, col = self.center

        drawn = False

        theta = 0
        while theta <= 360:

            rad = deg_to_rad(theta)

            dx = int(col + math.cos(rad) * self.radius)
            dy = int(row + math.sin(rad) * self.radius)

            if 0 <= dx < COLS and 0 <= dy < ROWS:
                matrix[dy, dx] = self.color
                drawn = True
            theta += delta

        return drawn


@register_effect
class ExplosionEffect(KeyboardProgram):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_explosions = 3
        self.explosions = self.make_explosions()
        self.clear_every_frame = False

    def get_name(self):
        return "Explosions"

    def get_description(self):
        return "Light and dark explosions that compliment each other."

    def get_cli_name(self):
        return "explosions"

    def get_author(self):
        return "explodes"

    def make_explosions(self, darken=1):
        return [self.make_explosion(darken=darken) for _ in range(self.num_explosions)]

    def make_explosion(self, darken=1):
        col = random.randint(0, COLS - 1)
        row = random.randint(0, ROWS - 1)
        # col = COLS // 2
        # row = ROWS // 2
        color = (
            random.randint(50, 255) // darken,
            random.randint(50, 255) // darken,
            random.randint(50, 255) // darken
        )
        return Explosion(center=(row, col), color=color)

    def init(self, kb):
        kb.brightness = 100

    def draw(self, kb, matrix, frame_num, dt):

        if frame_num % 15 == 0:
            # matrix.reset()
            self.explosions = self.make_explosions(darken=(frame_num % 2) * 15 + 1)

        for index, explosion in enumerate(self.explosions):
            explosion.expand()
            if not explosion.write_to(matrix):
                self.explosions[index] = self.make_explosion()


if __name__ == '__main__':
    effect = ExplosionEffect()
    effect.start()
