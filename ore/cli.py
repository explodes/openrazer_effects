from __future__ import print_function

import optparse
import sys

from ore.registry.registry import get_registry


class Program(object):

    def __init__(self):
        self.parser = optparse.OptionParser(usage="usage: %prog command [args...] [--audio-device=<device>]")
        self.parser.add_option(
            "-a",
            "--audio_device",
            dest="audio_device",
            default="default",
            help="name of the audio device to pair with, if used.")

    def _parse_and_execute(self, args):
        (opts, args) = self.parser.parse_args(args)

        if len(args) < 1:
            self._error("command required.")

        cmd = args[0]
        if len(cmd) > 0 and cmd[0] != '_' and hasattr(self, cmd) and callable(getattr(self, cmd)):
            func = getattr(self, cmd)
            func(*args, **vars(opts))
        else:
            self._error("invalid command {}".format(cmd))

    def _error(self, msg):
        self.parser.error(msg)

    def list(self, *args, **kwargs):
        reg = get_registry()
        for cli_name, effect in reg.items():

            effect = effect()

            details = {
                "cli": effect.get_cli_name(),
                "name": effect.get_name(),
                "author": effect.get_author(),
                "description": effect.get_description(),
                "type": effect.get_effect_type(),
            }
            if details["description"] is None:
                details["description"] = "No description."

            print("""{cli} :: {name} [{author}]
{description}
""".format(**details))

    def run(self, *args, **kwargs):
        if len(args) < 2:
            self._error("effect name required.")

        cli_name = args[1]
        reg = get_registry()
        if cli_name not in reg:
            self._error("effect {} not found".format(cli_name))

        effect_class = reg[cli_name]
        effect = effect_class(**kwargs)
        effect.start()


def main():
    prog = Program()
    prog._parse_and_execute(sys.argv[1:])
