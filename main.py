import emesh
import time
import os
from dotenv import load_dotenv

# INFO Initializing the emesh structure
def init():
    vars = preparse()
    emesh.connect(vars['port'])
    print("[emesh] Initialized")
    print("[emesh] Beaconing...")

# INFO Parsing our environment variables
def preparse():
    vars = {}
    # Parsing the port
    if not os.getenv('PORT') == "default":
        vars['port'] = os.getenv('PORT')
    return vars    

# INFO Entry point
if __name__ == "__main__":
    init()
    # Main cycle
    print("[MAIN CYCLE] Starting watchdog...")
    while not os.getenv('FORCE_QUIT'):
        # NOTE Reloading .env ensures that we can control the app cycle externally
        load_dotenv()
        emesh.beaconOn = os.getenv('BEACONING') # So we can even stop beaconing from here
        # NOTE As the scenarios can include long range radios, we have low bandwidth.
        # By waiting N seconds between beacons, we ensure that we are not beaconing
        # too often and spamming the radio channel with beacons.
        if emesh.beaconOn:
            print("[MAIN CYCLE] Beaconing is activated, proceeding...")
            emesh.beacon()
        else:
            print("[MAIN CYCLE] Beaconing is not activated, proceeding...")
        # Sleep for N seconds
        print("[MAIN CYCLE] Sleeping for " + os.getenv('BEACONING_INTERVAL') + " seconds")
        time.sleep(int(os.getenv('BEACONING_INTERVAL')))