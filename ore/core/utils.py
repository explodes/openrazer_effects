import sys
import time

import openrazer.client

COLS = 22
ROWS = 6


def find_keyboard():
    device_manager = openrazer.client.DeviceManager()

    for device in device_manager.devices:
        if device.type == 'keyboard':
            keyboard = device
            break
    else:
        print("Could not find suitable keyboard", file=sys.stderr)
        sys.exit(1)

    if not keyboard.has('lighting_led_matrix'):
        print("Keyboard doesnt have LED matrix", file=sys.stderr)
        sys.exit(1)

    return keyboard


def index_to_coord(index):
    index = index % (ROWS * COLS)
    col = index % COLS
    row = index // COLS
    return row, col


def int_to_color(v):
    r = (v & 0xff0000) >> 16
    g = (v & 0x00ff00) >> 8
    b = (v & 0xff)
    return r, g, b


class FpsLimiter(object):
    def __init__(self, max_fps=60):
        self.frame_start = time.time()
        self.wait = 1
        self.set_limit(max_fps)

    def start_frame(self):
        self.frame_start = time.time()

    def wait_for_next_frame(self):
        delay = self.wait - (time.time() - self.frame_start)
        if delay > 0:
            time.sleep(delay)

    def set_limit(self, max_fps):
        self.wait = 1 / max_fps

    def current_fps(self):
        return 1 / (time.time() - self.frame_start)
