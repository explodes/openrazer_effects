#!/usr/bin/env python3.6
from client.fx import Frame
from openrazer_effects.core.program import KeyboardProgram
from openrazer_effects.core.utils import *


def snake_order(row, col, top_left=True):
    if top_left and row % 2 == 0:
        return row, COLS - col - 1
    if not top_left and (row + 1) % 2 == 0:
        return row, COLS - col - 1
    return row, col


class Effect(KeyboardProgram):
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
