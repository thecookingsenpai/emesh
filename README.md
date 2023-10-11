# eMesh

## A human-usable fast and universal GUI for Meshtastic nodes

### What is eMesh?

eMesh is an interface initially made for myself to be able to better control, understand and play with devices used in the [Meshtastic Project](https://meshtastic.org/). A brief and absolutely not definitive list of supported devices is provided in the next section.

### Compatible devices

Any device that is compatible with the current Meshtastic for Python version should be supported without any problems. However, is important to note that our tests have been made against the following devices:

• LilyGo LORA32

### Features

- [x] A fully functional GUI for Meshtastic even if you are using the terminal (thanks [Textualize for its Textual library](https://github.com/Textualize/textual))
- [x] Serial Port connection (serial or usb over serial)
- [ ] Bluetooth connection (not yet, maybe not ever)
- [x] Support for beaconing (emitting a signal every X seconds)
	- [ ] Support for beaconing time customization
- [x] Possibility of specifying the serial port to use
- [x] Listening and showing messages in a clear and clean way
- [x] Easy to use chat-like interface with advanced commands


### Installation and usage

	git clone https://github.com/thecookingsenpai/emesh
	cd emesh
	pip install -r requirements.txt
	python gui.py

You can also play with term.py and emesh.py and use directly
	python term.py

If you really hate GUIs.

### License

MIT License

Copyright (c) 2023 TheCookingSenpai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
