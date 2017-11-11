# [OpenRazer effects](https://github.com/explodes/openrazer_effects)

A collection of effects to use with [OpenRazer](https://openrazer.github.io/)

## Installation

[Python 3.5+](https://www.python.org/downloads/release/python-350/) is required.

 - Virtual environments are always recommended.
 - `virtualenv --python="$(which python3.5)" venv && source venv/bin/activate`

Some additional packages are required for your system.

 - Install [OpenRazer](https://openrazer.github.io/)
 - Install other packages
   - Debian: `sudo apt install `

 - Install `openrazer_effects`
   - `pip install openrazer_effects`

## Usage

`openrazer_effects list`
List all effects

`openrazer_run <effect> [--audio-device=<device>]`
Run an effect for a specific audio device.

`openrazer_effects audiolist`
List available audio devices

`openrazer_effects audiotest`
Test capture of available audio devices. Can be crashy!!

## Contributing

Contributions are always welcome. Just send a PR!

## License

[GPLv2](https://github.com/explodes/openrazer_effects/blob/master/LICENSE)