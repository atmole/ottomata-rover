#! python3

"""
On-Board control application for the Mars Rover
"""

from mars_control import MarsControlMessage
from mars_hardware import MarsPCB
from time import sleep
import threading
import logging
from picamera import PiCamera
from datetime import datetime
import os


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
# logging.disable(logging.INFO)  # Uncomment to disable log messages

camera = PiCamera()
camera.resolution = (640, 480)
photo_interval = 10

datestamp = datetime.now()
folder_name_format = '{:%Y-%m-%d}_photos'
folder_name = folder_name_format.format(datestamp)
os.makedirs(folder_name, exist_ok=True)
logging.info('Created: {f}'.format(f=folder_name))


# FUNCTIONS
def execute_command():
    while(mc_server.keepalive):
        if mc_server.switch_3:  # direction
            fwd = True
            logging.info('Forward movement')
            mh_server.LIGHT.on()
        else:
            fwd = False
            logging.info('Reverse movement')
            mh_server.LIGHT.off()
        if mc_server.switch_1:
            mh_server.MOSFET1_G.on()
            logging.info('Left drive enabled')
        else:
            mh_server.MOSFET1_G.off()
            logging.info('Left drive disabled')
        if mc_server.switch_2:
            mh_server.MOSFET2_G.on()
            logging.info('Right drive enabled')
        else:
            mh_server.MOSFET2_G.off()
            logging.info('Right drive disabled')

        if mc_server.switch_1 or mc_server.switch_2:
            mh_server.make_steps(forward=fwd)
            logging.info('Stepper ON')
        else:
            logging.info('Stepper OFF')
            sleep(1)

        if mc_server.switch_4:
            if mc_server.button_1:
                mh_server.pickup()
                logging.info('Sample collection')
            elif mc_server.button_2:
                mh_server.unload()
                logging.info('Unload samples')
        else:
            if mc_server.button_1:
                logging.info('Manual lowering')
                mh_server.MOSFET3_G.on()
                while(mc_server.button_1):
                    mh_server.make_steps(forward=True)
                mh_server.MOSFET3_G.off()
            elif mc_server.button_2:
                logging.info('Manual lifting')
                mh_server.MOSFET3_G.on()
                while(mc_server.button_2 and not mh_server.SWITCH_6.value):
                    mh_server.make_steps(forward=False)
                mh_server.MOSFET3_G.off()

        mc_server.batteryv = mh_server.BATTERY.value*12
        mc_server.lightsen = mh_server.AMBIENT.value
        logging.info('Battery: {bat} Light: {light}'
                     .format(bat=mc_server.batteryv, light=mc_server.lightsen))
        mh_server.steptime = 1/(mc_server.potmeter * 3)
        logging.info('Steptime: {s}'.format(s=mh_server.steptime))
        logging.info('loop end'.center(20, '-'))


def take_photos():
    while(mc_server.keepalive):
        raw_timestamp = datetime.now()
        filename_format = '{:%Y-%m-%d_%H-%M-%S}.jpg'
        filename = filename_format.format(raw_timestamp)
        camera.start_preview()
        sleep(2)  # Camera warm-up time
        camera.capture(os.path.join(folder_name, filename))
        sleep(photo_interval)


mc_server = MarsControlMessage(host='192.168.2.10')
mh_server = MarsPCB(steprefresh=1)

logging.info('Testing the inputs and outputs on the rover')
mh_server.check_inputs()
mh_server.check_outputs()
logging.info('Creating the socket')
mc_server.create_socket()

t1 = threading.Thread(target=mc_server.serv)
t2 = threading.Thread(target=execute_command)
t3 = threading.Thread(target=take_photos)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

mc_server.close()
mh_server.close_gpio_objects()
