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

No licenses, this one is free software
