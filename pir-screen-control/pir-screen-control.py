#
# Code initially taken from these projects:
#   https://www.hackster.io/hardikrathod/pir-motion-sensor-with-raspberry-pi-415c04
#   https://github.com/Shmoopty/rpi-appliance-monitor
# . https://github.com/sujal/rpi-appliance-monitor
# 

import sys
import time
import logging
import threading
import RPi.GPIO as GPIO
import signal
import paho.mqtt.publish as mqttpublish
import vcgencmd

from time import localtime, strftime
from ConfigParser import SafeConfigParser
from vcgencmd import Vcgencmd


def turn_off_screen():
    vcgm = Vcgencmd()
    output = vcgm.display_power_off(screen_id)
    logging.info('Turning off screen')
    notify_screen_state('Turning off screen')


def turn_on_screen():
    vcgm = Vcgencmd()
    output = vcgm.display_power_on(screen_id)
    logging.info('Turning on screen')
    notify_screen_state('Turning on screen')


def notify_screen_state(msg):
    if len(msg) > 1:
        logging.info(msg)
        if len(mqtt_topic) > 0:
            mqtt(msg)


def mqtt(msg):
    try:

        msg_body = {
            'message': msg,
            'last_motion_time': last_motion_time,
            'start_motion_time': start_motion_time,
            'motion_active': motion_active
        }
        # this is the basic msg
        msgs = [{'topic': mqtt_topic, 'payload': json.dumps(msg_body), 'qos': 0, 'retain': True}]

        mqtt_send_messages(msgs)

    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pass

def mqtt_send_messages(msgs):
    try:
        mqtt_auth = None

        logging.debug('about to send messages: ' + json.dumps(msgs))

        if len(mqtt_username) > 0:
            mqtt_auth = { 'username': mqtt_username, 'password': mqtt_password }        

        mqttpublish.multiple(msgs, hostname=mqtt_hostname, port=mqtt_port, client_id=mqtt_clientid,
        keepalive=60, will=None, auth=mqtt_auth, tls=None)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        pass

def heartbeat():
    global motion_active
    global screen_active_timelimit
    
    current_time = time.time()
    logging.info("HB at {}".format(current_time))

    # if we're currenting in a motion state, check if we're over the time linit
    # and shutoff the screen if so.
    if (motion_active 
            and current_time - last_motion_time > screen_active_timelimit):
        motion_active = False
        turn_off_screen()

    threading.Timer(1, heartbeat).start()

def motion_detected(x):
    global motion_active
    global last_motion_time
    global start_motion_time

    last_motion_time = time.time()

    logging.debug('Motion detected at {}'.format(last_motion_time))

    if not motion_active:
        start_motion_time = last_motion_time
        motion_active = True
        turn_on_screen()

def exit_gracefully(x,y):
    logging.info('Exiting gracefully...')
    GPIO.cleanup()

signal.signal(signal.SIGINT, exit_gracefully)
signal.signal(signal.SIGTERM, exit_gracefully)

logging.basicConfig(format='%(message)s', level=logging.INFO)

if len(sys.argv) == 1:
    logging.critical("No config file specified")
    sys.exit(1)


motion_active = False
last_motion_time = time.time()
start_motion_time = last_motion_time

config = SafeConfigParser()
config.read(sys.argv[1])
verbose = config.getboolean('main', 'VERBOSE')
sensor_pin = config.getint('main', 'SENSOR_PIN')
screen_id = config.getint('main', 'screen_id')
screen_active_timelimit = config.getint('main', 'screen_active_timelimit')

# mqtt config
mqtt_hostname = config.get('mqtt', 'mqtt_hostname')
mqtt_port = config.get('mqtt', 'mqtt_port')
mqtt_topic = config.get('mqtt', 'mqtt_topic')
mqtt_username = config.get('mqtt', 'mqtt_username')
mqtt_password = config.get('mqtt', 'mqtt_password')
mqtt_clientid = config.get('mqtt', 'mqtt_clientid')

if verbose:
    logging.getLogger().setLevel(logging.DEBUG)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN) #PIR
GPIO.add_event_detect(sensor_pin, GPIO.RISING)
GPIO.add_event_callback(sensor_pin, motion_detected)

logging.info('Running config file {} monitoring GPIO pin {}'\
      .format(sys.argv[1], str(sensor_pin)))
threading.Timer(1, heartbeat).start()