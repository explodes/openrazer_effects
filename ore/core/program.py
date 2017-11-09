import time
import typing

from openrazer.client.devices.keyboard import RazerKeyboard
from openrazer.client.fx import Frame
from ore.core.effects import KeyboardEffect
from ore.core.utils import FpsLimiter, find_keyboard, MAX_FPS


class KeyboardProgram(KeyboardEffect):

    def __init__(self, max_fps=MAX_FPS, debug=False):
        self.max_fps = max_fps
        self.fps = FpsLimiter(max_fps)
        self.debug = debug
        self.clear_every_frame = True

        self.keyboard = find_keyboard()

        self.log("fps target: {}".format(self.fps.wait))

    def log(self, *args):
        if self.debug:
            print(*args)

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
                self.log("stopped at frame {0} with time delta {1}".format(frame, time_delta))
                break

            if frame % self.max_fps == 0:
                self.log("at frame {0} with time delta {1}".format(frame, time_delta))

            self.fps.wait_for_next_frame()
            frame += 1

    def init(self, kb: RazerKeyboard):
        pass

    def draw(self, kb: RazerKeyboard, matrix: Frame, frame_num: int, dt: float) -> typing.Any:
        return False
