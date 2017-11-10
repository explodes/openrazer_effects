#!/usr/bin/env python3.6
import typing

from openrazer.client.devices.keyboard import RazerKeyboard
from openrazer.client.fx import Frame
from ore.core.program import KeyboardProgram
from ore.core.utils import ROWS, COLS, index_to_coord
from ore.registry.registry import register_effect


def snake_order(row, col, top_left=True):
    if top_left and row % 2 == 0:
        return row, COLS - col - 1
    if not top_left and (row + 1) % 2 == 0:
        return row, COLS - col - 1
    return row, col


@register_effect
class Effect(KeyboardProgram):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_name(self):
        return "Double Snakes"

    def get_description(self):
        return "Two winding snakes that chase each other around the keyboard."

    def get_cli_name(self):
        return "snakes"

    def get_author(self):
        return "explodes"

    def init(self, kb: RazerKeyboard):
        kb.brightness = 100

    def draw(self, kb: RazerKeyboard, matrix: Frame, frame_num: int, dt: float) -> typing.Any:
        snake_len = (ROWS * COLS) // 5
        snake_div = int(255 / snake_len)

        for i in range(snake_len):
            row, col = index_to_coord(frame_num + i)
            row, col = snake_order(row, col)
            matrix[row, col] = (snake_div * i, 255 - snake_div * i, 0)

        for i in range(snake_len):
            row, col = index_to_coord(frame_num + i + (ROWS * COLS) // 2)
            row, col = snake_order(row, col, top_left=False)
            matrix[row, col] = (0, snake_div * i, 255 - snake_div * i)


if __name__ == '__main__':
    effect = Effect(debug=True)
    effect.start()
