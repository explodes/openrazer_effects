import time
import typing

from openrazer.client.devices.keyboard import RazerKeyboard
from openrazer.client.fx import Frame
from ore.core.effects import KeyboardEffect
from ore.core.utils import FpsLimiter, find_keyboard

MAX_FPS = 35


class KeyboardProgram(KeyboardEffect):

    def __init__(self, **kwargs):
        super(KeyboardEffect, self).__init__(**kwargs)
        self.fps = FpsLimiter(MAX_FPS)
        self.clear_every_frame = True

        self.keyboard = find_keyboard()

    def start(self):
        self.init(self.keyboard)
        self.loop(self.keyboard)

    def loop(self, kb: RazerKeyboard):

        stop = False
        last_timestamp = time.time()
        frame = 0

        while not stop:
            self.fps.start_frame()

            now = time.time()
            time_delta = now - last_timestamp
            last_timestamp = now

            if self.clear_every_frame:
                kb.fx.advanced.matrix.reset()

            stop = self.draw(kb, kb.fx.advanced.matrix, frame, time_delta)
            kb.fx.advanced.draw()

            if stop:
                break

            self.fps.wait_for_next_frame()
            frame += 1

    def init(self, kb: RazerKeyboard):
        raise NotImplementedError()

    def draw(self, kb: RazerKeyboard, matrix: Frame, frame_num: int, dt: float) -> typing.Any:
        raise NotImplementedError()
