import emesh
import time
import os
from dotenv import load_dotenv

# SECTION GUI Variables
outputs = ""
last_output = ""

messageToShow = ""
last_messageToShow = ""

forceQuit = False
# !SECTION GUI Variables

beaconCooldown = 0

import builtins as __builtin__
# Overriding print for the GUI
def print(*args, **kwargs):
    global outputs
    outputs = "".join(map(str, args))
    __builtin__.print(*args, **kwargs)

# INFO Initializing the emesh structure
def init():
    print("[SYSTEM] Starting EMesh...")
    vars = preparse()
    emesh.connect(vars['port'])
    print("[LOADER] Initialized")

# INFO Parsing our environment variables
def preparse():
    vars = {}
    # Parsing the port
    if not os.getenv('PORT') == "default":
        vars['port'] = os.getenv('PORT')
    return vars    

def main():
    global beaconCooldown
    global messageToShow
    global forceQuit
    # INFO Entry point
    init()
    # Main cycle
    print("[MAIN CYCLE] Starting watchdog...")
    was_connected = False
    while not ((os.getenv('FORCE_QUIT')=="True") or forceQuit):
        # This is just a way to check if we need to notify the gui
        are_connected = emesh.connected
        if (are_connected!= was_connected):
            print("[GUI] Changed connection status")
            messageToShow = "CONNECTION ESTABLISHED"
        # NOTE Reloading .env ensures that we can control the app cycle externally
        load_dotenv()
        emesh.beaconOn = (os.getenv('BEACONING')=="True") # So we can even stop beaconing from here
        emesh.beaconOn = emesh.beaconingPrioritySettings # GUI variables are prioritized
        print("[MAIN CYCLE] Beaconing: " + str(emesh.beaconOn))
        # NOTE As the scenarios can include long range radios, we have low bandwidth.
        # By waiting N seconds between beacons, we ensure that we are not beaconing
        # too often and spamming the radio channel with beacons.
        if emesh.beaconOn:
            print("[MAIN CYCLE] Checking for beacon cooldown...")
            # The following keeps the code running while we cooldown beaconing too
            if (beaconCooldown > 0):
                isMultipleOfTen = (beaconCooldown % 10 == 0)
                if isMultipleOfTen:
                    print("[MAIN CYCLE] Beacon cooldown: " + str(beaconCooldown))
                beaconCooldown -= 1
            else:
                print("[MAIN CYCLE] Beaconing is activated, proceeding...")
                beaconCooldown = int(os.getenv('BEACONING_INTERVAL'))
                emesh.beacon()
                print("[MAIN CYCLE] Beacon emitted. Proceeding to the next cycle...")
        else:
            print("[MAIN CYCLE] Beaconing is not activated, proceeding...")
        # Sleep for N seconds
        # print("[MAIN CYCLE] Sleeping for " + os.getenv('SLEEP_INTERVAL') + " seconds")
        time.sleep(int(os.getenv('SLEEP_INTERVAL')))
        # print("[MAIN CYCLE] Sleeping complete. Proceeding to the next cycle...")
        
print("[SYSTEM] Ready to start.")


if __name__ == "__main__":
    main()