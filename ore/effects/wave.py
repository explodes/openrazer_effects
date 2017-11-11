import math
import random

from openrazer.client.devices.keyboard import RazerKeyboard
from openrazer.client.fx import Frame
from ore.core.program import KeyboardProgram
from ore.core.utils import ROWS, COLS
from ore.registry.registry import register_effect


@register_effect
class Wave(KeyboardProgram):

    def get_name(self):
        return "Wave"

    def get_cli_name(self):
        return "wave"

    def get_author(self):
        return "explodes"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0
        self.random = random.Random()

    def init(self, kb: RazerKeyboard):
        kb.brightness = 100

    def draw(self, kb: RazerKeyboard, matrix: Frame, frame_num: int, dt: float):
        RPS = 1  # revolutions per second
        CPS = 0.25  # color revolutions per second
        self.time += COLS * dt * RPS

        theta = math.pi / ROWS
        offset = theta * self.time

        for col in range(COLS):
            mid_point = int((math.sin(theta * col + offset) + 1) / 2 * (ROWS + 1))

            for y in range(0, ROWS):
                if ROWS <= y < 0:
                    continue

                if y < mid_point:
                    color_wave = (math.sin(self.time * CPS) + 1) / 2
                    matrix[y, col] = (255 * color_wave, 10 * y, 20 * color_wave)
                else:
                    color_wave = (math.sin(self.time * CPS / 2) + 1) / 2
                    matrix[y, col] = (0, 50 + 50 * color_wave, ROWS * 5 - 5 * y)


if __name__ == "__main__":
    effect = Wave()
    effect.start()
