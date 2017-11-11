# [OpenRazer effects](https://github.com/explodes/openrazer_effects)

A collection of effects to use with [OpenRazer](https://openrazer.github.io/)

## Installation

 - Install [OpenRazer](https://openrazer.github.io/)
 - Install other packages
   - Debian Python 3.6: `sudo apt install python3.6-dev portaudio19-dev libdbus-1-dev libdbus-glib-1-dev`

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