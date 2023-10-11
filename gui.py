import json
import os
import time
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from textual.widgets import Input, Label, Pretty
from textual.widgets import Button, Static, RichLog, Sparkline, Checkbox
from textual.containers import Horizontal, VerticalScroll
from textual.validation import Function, Number, ValidationResult, Validator
from textual import events, on
import threading
import term
from dotenv import load_dotenv


class MeshTerm(App):
    CSS_PATH = "meshterm.tcss"

    stopWatchdog = False
    messageToShow = None

    # INFO Composing the app
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        # Inputs

        yield Horizontal(VerticalScroll(
            Label("Enter the serial port to connect to: "),
            Input(placeholder="/dev/ttyUSB0", id="port"),
            Button("Connect to radio", id="connect"),
            Checkbox("Enable beaconing:", True, id="beaconingBox"),
            
        ),
            VerticalScroll(
                Label("Unknown Radio Name", id="radio_name"),
                Label(""),
                Input(placeholder="Send something...", id="msg"),
                Button("Send", id="send", disabled=True)
        ))
        
        yield Horizontal(VerticalScroll(
            Button("Exit", id="exit"),
            Label("CONNECTED RADIO INFO"),
            VerticalScroll(
                Label("No radio connected", id="radio_namebox"),
                Label("", id="radio_id"),
                Label("", id="radio_user"),
            )
        ),
            VerticalScroll(
            Sparkline([1, 2, 3, 3, 3, 3, 3], summary_function=min,),
            Label("Received messages:"),
            RichLog(id="received_messages", auto_scroll=True)
        ))
        yield Label("", id="message_to_show")
        yield Sparkline([1, 2, 3, 3, 3, 3, 3, 3, 4, 4, 5, 5, 6, 5, 5, 4, 4, 3, 3, 3, 3, 3, 3, 3, 2, 1], summary_function=min,)
        # Main log
        yield RichLog(id="main_log", auto_scroll=True)

        # NOTE Here we start the watcher thread
        self.watchdog = threading.Thread(name="watchdog", target=self.watcher)
        self.watchdog.start()

    # SECTION Actions

    def on_key(self, event: events.Key) -> None:
        """Handle key events."""
        pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button events."""
        text_log = self.query_one("#main_log")
        action = str(event.button.id).lower()
        if action == "exit":
            try:
                term.forceQuit = True
                self.stopWatchdog = True
            except:
                print("[SYSTEM] Failed to stop thread")
            exit(1)
        elif action == "connect":
            self.connect()
        elif action == "send":
            self.send()

    # INFO Sending a message to the device
    def send(self):
        if not term.emesh.connected:
            self.messageToShow = "CANNOT SEND MESSAGE: No connection"
            return
        textToSend = self.query_one("#msg").value
        term.emesh.sendRaw(textToSend)
        self.query_one("#msg").value = ""
        self.messageToShow = "MESSAGE SENT: " + textToSend
        self.query_one("#main_log").write(self.messageToShow)
        self.query_one("#received_messages").write("[You] > " + textToSend)
    
    # INFO Managing connection to the device
    def connect(self):
        self.query_one("#connect").disabled = True
        self.query_one("#connect").value = "CONNECTING..."
        self.port = self.query_one("#port").value
        self.port = self.port.strip()
        self.messageToShow = "CONNECTING TO " + self.port + "..."
        if not self.port or self.port == "":
            self.port = None
        self.instance = threading.Thread(target=term.main)
        self.instance.start()

    def change_value(self, id, replacement):
        self.query_one(id).update(replacement)
    # !SECTION Actions
    
    def loadEnv(self):
        self.env = {}
        with open(".env", "r") as f:
            textenv = f.readlines()
            for line in textenv:
                key, value = line.split("=")
                self.env[key.strip()] = value.strip()
        return self.env

    def saveEnv(self):
        preparedEnv = ""
        for key, value in self.env.items():
            preparedEnv += key + "=" + value + "\n"
        with open(".env", "w") as f:
            f.write(preparedEnv)
            f.flush()
        return self.env
            

    def watcher(self):
        while not self.stopWatchdog:
            time.sleep(1)
            # Refreshing the environment variables and setting ours if needed
            try:
                term.emesh.beaconingPrioritySettings = self.query_one("#beaconingBox").value
            except Exception as e:
                print("[WARNING] beaconingBox element is not reachable - this may be temporary.")
            # Loading messages into the gui
            try:
                if (term.outputs != term.last_output):
                    term.last_output = term.outputs
                    self.query_one("#main_log").write(term.outputs)
                # Priority to us here
                if (self.messageToShow):
                    messageToShow = self.messageToShow
                    self.messageToShow = None
                else:
                    messageToShow = term.messageToShow
                self.change_value("#message_to_show", messageToShow)
                # If we are connected we should get our variables
                if term.emesh.connected:
                    name = term.emesh.interface.getShortName()
                    self.query_one("#connect").disabled = False
                    self.query_one("#connect").value = "Reconnect"
                    self.query_one("#radio_name").update("Connected to: " + name)
                    self.query_one("#send").disabled = False
                    # Also updating our infos
                    self.query_one("#radio_namebox").update("Radio NAME: " + name)
                    self.query_one("#radio_id").update("Radio ID (long name): " + str(term.emesh.interface.getLongName()))
                    self.query_one("#radio_user").update("Radio USER: " + str(term.emesh.interface.getMyUser()))
                # Populating the received messages
                for receivd in term.emesh.msg_received:
                    if receivd["portnum"] == "TEXT_MESSAGE_APP":
                        headerMessage = "[" + str(receivd["from"]) + " -> " + str(receivd["to"]) + "] > " 
                        textToShow = headerMessage + receivd["text"]
                        self.query_one("#received_messages").write(textToShow)
                term.emesh.msg_received = []
            except Exception as e:
                self.change_value("#message_to_show", "ERROR: " + str(e))


if __name__ == "__main__":
    app = MeshTerm()
    app.run()
