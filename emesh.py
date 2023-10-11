import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import time
# Helpers
from hashlib import sha256
import keys
import json

serial_port = None
interface = None

beaconOn = False
beaconingPrioritySettings = False # Only for GUI usage, comment out if you don't want to use the GUI

sbnum = 0

connected = False

msg_received = []

# NOTE Just an easy wrapper around sha256
def hash(input):
    return sha256(input.encode('utf-8')).hexdigest()

def onReceive(packet, interface):
    global msg_received
    print("[RECEIVED] Received packet: " + str(packet))
	# called when a packet arrives
    try:
        decoded = packet["decoded"]
        decoded["from"] = packet["from"]
        decoded["to"] = packet["to"]
    except:
        print("[ERROR] Could not decode packet: discarding it")
        return
	# ANCHOR We have received a packet and we decoded it
    print(decoded)
    # Let's take the type of the packet
    packet_type = decoded["portnum"]
    print("Received packet type: " + packet_type)
    msg_received.append(decoded)

def onConnection(interface, topic=pub.AUTO_TOPIC):
    global connected
	# called when we (re)connect to the radio
	# defaults to broadcast, specify a destination ID if you wish
    connected = True
    theName =  json.dumps(interface.getShortName())
    interface.sendText(theName + " greets you!")

# INFO Monitor and, if applicable, start beaconing using encrypted messages or plaintext messages
def beacon(encrypted=False):
        # If we are supposed to be beaconing, we need to send a beacon and wait 10 seconds
        print("[BEACONING] Sending beacon...")
        # NOTE Generating a beacon first
        our_info = interface.getShortName()
        our_timestamp = int(time.time())
        global bnum
        bnum += 1
        beacon = {
            "type": "beacon",
            "number": bnum,
            "timestamp": our_timestamp,
            "info": our_info
        }
        interface.sendText(json.dumps(beacon))
        print("[BEACONING] Beacon sent: " + json.dumps(beacon))

def sendRaw(raw):
    print("[SEND RAW] Sending raw: " + raw)
    interface.sendText(raw)
    print("[SEND RAW] Raw sent: " + raw)

def sendRawBytes(raw):
    print("[SEND RAW BYTES] Sending raw: " + raw)
    interface.sendBytes(raw)
    print("[SEND RAW BYTES] Raw sent: " + raw)

def connect(serialPort=None):
    global serial_port
    global interface
    # Ensuring we have an identity
    keys.ensure()
    # Connecting to the radio
    serial_port = serialPort
    pub.subscribe(onReceive, "meshtastic.receive")
    pub.subscribe(onConnection, "meshtastic.connection.established")
    interface = meshtastic.serial_interface.SerialInterface(serial_port)
    print("[INITIALIZATION] Connection to radio established")