import pyaudio

from openrazer_effects.audio.capture import DeviceGraph
from openrazer_effects.core.program import RazerKeyboard
from openrazer_effects.core.utils import find_keyboard, COLS, ROWS


class Effect(object):

    def __init__(self, device_name):
        p = pyaudio.PyAudio()
        self.graph = DeviceGraph(p, device_name, buckets=14)
        self.keyboard = find_keyboard()

    def start(self):
        kb = self.keyboard
        self.init(kb)
        while True:
            kb.fx.advanced.matrix.reset()
            if not self.loop(self.keyboard):
                break
            kb.fx.advanced.draw()

    def init(self, kb: RazerKeyboard):
        kb.brightness = 100

    def loop(self, kb: RazerKeyboard):
        self.graph.read_row()
        values = self.graph.histogram.values[:11]

        matrix = kb.fx.advanced.matrix

        half = COLS // 2

        for col, p in enumerate(values):
            self.draw_column(matrix, half - col, p)
            self.draw_column(matrix, half + col, p)

        return True

    def draw_column(self, matrix, col, p):
        limit = int((1 - p) * ROWS) - 1
        for row in range(ROWS - 1, limit, -1):
            color = self.color_for_volume(row, p)
            # print("m[{},{}] = {}".format(row, col, color))
            matrix[row, col] = color
        for row in range(limit, -1, -1):
            color = self.empty_color_for_volume(row, p)
            matrix[row, col] = color

    def color_for_volume(self, row, p):
        return (
            255 * (p ** 2),
            255 * (row / ROWS),
            20 * (row / ROWS),
        )

    def empty_color_for_volume(self, row, p):
        return (
            20 * (row / ROWS),
            128 * (p ** 2),
            128 * (row / ROWS),
        )


if __name__ == '__main__':
    effect = Effect("pulse")
    effect.start()
