#! python3

"""
On-Board control application for the Mars Rover
"""

from mars_control import MarsControlMessage
from mars_hardware import MarsPCB
from time import sleep
import threading
import logging
# from picamera import PiCamera
# from datetime import datetime
# import os


logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logging.disable(logging.INFO)  # Uncomment to disable log messages

# CAMERA
# camera = PiCamera()
# camera.resolution = (640, 480)
# photo_interval = 15
# datestamp = datetime.now()
# folder_name_format = '{:%Y-%m-%d_%H}h_photos'
# folder_name = folder_name_format.format(datestamp)
# cam_folder = os.path.join('camera', folder_name)
# os.makedirs(cam_folder, exist_ok=True)
# logging.info('Created: {f}'.format(f=folder_name))


# FUNCTIONS
def execute_command():
    while(msg_ob.keepalive):
        if msg_ob.switch_3:  # direction
            fwd = True
            logging.info('Reverse movement')
            hw_ob.LIGHT.off()
        else:
            fwd = False
            logging.info('Forward movement')
            hw_ob.LIGHT.on()
        if msg_ob.switch_1:
            hw_ob.MOSFET1_G.on()
            logging.info('Left drive enabled')
        else:
            hw_ob.MOSFET1_G.off()
            logging.info('Left drive disabled')
        if msg_ob.switch_2:
            hw_ob.MOSFET2_G.on()
            logging.info('Right drive enabled')
        else:
            hw_ob.MOSFET2_G.off()
            logging.info('Right drive disabled')

        if msg_ob.switch_1 or msg_ob.switch_2:
            hw_ob.make_steps(forward=fwd)
            logging.info('Stepper ON')
        else:
            logging.info('Stepper OFF')
            sleep(1)

        if msg_ob.switch_4:
            if msg_ob.button_1:
                hw_ob.pickup()
                logging.info('Sample collection')
            elif msg_ob.button_2:
                hw_ob.unload()
                logging.info('Unload samples')
        else:
            if msg_ob.button_1:
                logging.info('Manual lowering')
                hw_ob.MOSFET3_G.on()
                while(msg_ob.button_1):
                    hw_ob.make_steps(forward=True)
                hw_ob.MOSFET3_G.off()
            elif msg_ob.button_2:
                logging.info('Manual lifting')
                hw_ob.MOSFET3_G.on()
                while(msg_ob.button_2 and not hw_ob.SWITCH_6.value):
                    hw_ob.make_steps(forward=False)
                hw_ob.MOSFET3_G.off()

        msg_ob.batteryv = hw_ob.BATTERY.value*12
        msg_ob.lightsen = hw_ob.AMBIENT.value
        logging.info('Battery: {bat} Light: {light}'
                     .format(bat=msg_ob.batteryv, light=msg_ob.lightsen))
        hw_ob.steptime = 1/(msg_ob.potmeter * 7)
        logging.info('Steptime: {s}'.format(s=hw_ob.steptime))
        logging.info('loop end'.center(20, '-'))


# def take_photos():
#     while(msg_ob.keepalive):
#         raw_timestamp = datetime.now()
#         filename_format = '{:%Y-%m-%d_%H-%M-%S}.jpg'
#         filename = filename_format.format(raw_timestamp)
#         camera.start_preview()
#         sleep(2)  # Camera warm-up time
#         camera.capture(os.path.join(cam_folder, filename))
#         sleep(photo_interval)


msg_ob = MarsControlMessage(host='192.168.2.10')
hw_ob = MarsPCB(steprefresh=0.5)

logging.info('Testing the inputs and outputs on the rover...')
hw_ob.check_inputs()
hw_ob.check_outputs()
logging.info('Creating the socket...')
msg_ob.create_socket()

t1 = threading.Thread(target=msg_ob.serv)
t2 = threading.Thread(target=execute_command)
# t3 = threading.Thread(target=take_photos)

t1.start()
t2.start()
# t3.start()

t1.join()
t2.join()
# t3.join()

msg_ob.close()
hw_ob.close_gpio_objects()
