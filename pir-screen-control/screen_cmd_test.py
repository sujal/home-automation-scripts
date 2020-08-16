import sys
import time
import vcgencmd
from vcgencmd import Vcgencmd

if len(sys.argv) == 1:
    logging.critical("No screen_id specified")
    sys.exit(1)

screen_id = int(sys.argv[1])

def turn_off_screen():
    print('turning off screen')
    vcgm = Vcgencmd()
    output = vcgm.display_power_off(screen_id)


def turn_on_screen():
    print('turning on screen')
    vcgm = Vcgencmd()
    output = vcgm.display_power_on(screen_id)

vcgm = Vcgencmd()
for x in [0,1,2,3,7]:
    print('{}: {}'.format(x, vcgm.display_power_state(x)))

turn_off_screen()
time.sleep(5)
turn_on_screen()
time.sleep(5)
turn_off_screen()
time.sleep(5)
turn_on_screen()
