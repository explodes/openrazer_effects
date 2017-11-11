import struct
import threading
from queue import Queue

import numpy
import pyaudio


class DeviceFinder(object):
    def __init__(self, p):
        self.p = p

    def find_output_devices(self):
        """
        Find devices suitable for writing.
        """
        for device in self.devicesiter():
            if device["maxOutputChannels"] > 0:
                yield device

    def find_input_devices(self):
        """
        Find devices suitable for recording.
        """
        for device in self.devicesiter():
            if device["maxInputChannels"] > 0:
                yield device

    def find_named_device(self, name):
        for device in self.devicesiter():
            if device["name"] == name:
                return device
        raise ValueError("device {} not found".format(name))

    def devicesiter(self):
        count = self.p.get_device_count()
        for index in range(count):
            device = self.p.get_device_info_by_index(index)
            yield device


class DeviceReader(object):

    def __init__(self, p, device):
        self.p = p
        self.device = device

    def stream_output(self, buffer_size=2 ** 10):
        return self.create_stream(is_input=False, buffer_size=buffer_size)

    def stream_input(self, buffer_size=2 ** 10):
        return self.create_stream(is_input=True, buffer_size=buffer_size)

    def create_stream(self, is_input, buffer_size):
        stream = AudioStream(self.device)

        thread = threading.Thread(
            name="device-thread-{}".format(self.device["name"]),
            target=self._start_stream,
            args=(stream, is_input, buffer_size),
            daemon=True)
        thread.start()

        return stream

    def _generate_null_stream(self, stream):
        import time

        while True:
            stream(b"\x00" * 304, 0, 0, 0)
            time.sleep(0.2)

    def _start_stream(self, stream, is_input, buffer_size):
        self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=int(self.device.get("defaultSampleRate", 44100)),
            input=is_input,
            output=not is_input,
            frames_per_buffer=buffer_size,
            input_device_index=self.device["index"],
            stream_callback=stream)


class AudioStream(object):
    flags = {
        pyaudio.paInputUnderflow: "paInputUnderflow",
        pyaudio.paInputOverflow: "paInputOverflow",
        pyaudio.paOutputUnderflow: "paOutputUnderflow",
        pyaudio.paOutputOverflow: "paOutputOverflow",
        pyaudio.paPrimingOutput: "paPrimingOutput",
    }

    def __init__(self, device):
        self.device = device
        self.closed = False
        self.queue = Queue()

    def __call__(self, in_data, frame_count, time_info, status):
        if status == 0:
            self.queue.put(in_data, block=True)
        return None, pyaudio.paComplete if self.closed else pyaudio.paContinue

    def __iter__(self):
        while True:
            value = self.queue.get(block=True)
            if self.closed:
                break
            yield value

    def close(self):
        self.closed = True


class AudioAnalyzer(object):

    def __init__(self, buckets=6, scale=10, exponent=1):
        self.buckets = buckets
        self.scale = scale
        self.exponent = exponent

    def calculate_levels(self, data):
        # Use FFT to calculate volume for each frequency

        # Convert raw sound data to Numpy array
        fmt = "%dH" % (len(data) // 2)
        data2 = struct.unpack(fmt, data)
        data2 = numpy.array(data2, dtype='h')

        # Apply FFT
        fourier = numpy.fft.fft(data2)
        ffty = numpy.abs(fourier[0:len(fourier) // 2]) / 1000
        ffty1 = ffty[:len(ffty) // 2]
        ffty2 = ffty[len(ffty) // 2::] + 2
        ffty2 = ffty2[::-1]
        ffty = ffty1 + ffty2
        ffty = numpy.log(ffty) - 2

        fourier = list(ffty)[4:-4]
        fourier = fourier[:len(fourier) // 2]

        size = len(fourier)

        # Add up for 6 lights
        levels = [sum(fourier[i:(i + size // self.buckets)]) for i in range(0, size, size // self.buckets)][
                 :self.buckets]

        return self._normalize_levels(levels)

    def _normalize_levels(self, levels):
        out = [0] * len(levels)
        lo = min(levels)
        hi = max(levels)
        if lo == hi:
            return out
        for index, level in enumerate(levels):
            p = (level - lo) / (hi - lo)
            out[index] = p ** self.exponent
        return out


class Histogram(object):
    BOXES = ('\u2581', '\u2582', '\u2583', '\u2584', '\u2585', '\u2586', '\u2587', '\u2588')

    def __init__(self, size):
        self.size = size
        self.values = [0] * size

    def set_values(self, values):
        self.values = values

    def _char(self, index):
        percentage = self.values[index]
        char_index = int((len(Histogram.BOXES) - 1) * percentage)
        return Histogram.BOXES[char_index]

    def __str__(self):
        return u"".join(self._char(index) for index in range(self.size))


class DeviceGraph(object):

    def __init__(self, p, device_name, buffer_size=2 ** 11, buckets=64):
        self.device_name = device_name

        finder = DeviceFinder(p)
        device = finder.find_named_device(device_name)
        self.analyzer = AudioAnalyzer(buckets=buckets)
        self.reader = DeviceReader(p, device)
        self.histogram = Histogram(buckets)
        self.stream = self.reader.stream_input(buffer_size=buffer_size)
        self.stream_data = iter(self.stream)

    def read_row(self):
        try:
            data = next(self.stream_data)
        except StopIteration:
            return
        else:
            levels = self.analyzer.calculate_levels(data)
            self.histogram.set_values(levels)

    def close(self):
        self.stream.close()


def counter(initial=0, step=1):
    i = initial
    while True:
        yield i
        i += step


def graph_audio_devices(p, device_names, buffer_size=2 ** 11, buckets=32):
    if not device_names:
        raise ValueError("device_names must be a list of device names.")

    graphs = [DeviceGraph(
        p,
        device_name,
        buffer_size=buffer_size,
        buckets=buckets)
        for device_name in device_names]

    for index in counter():
        print("{:>5}".format(index), end=" :: ")
        for graph in graphs:
            graph.read_row()
            print("{}: {}".format(graph.device_name, graph.histogram), end=" ")
        print("\n", end="")
