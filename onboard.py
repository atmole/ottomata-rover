#! python3

"""
On-Board control application for the Mars Rover
"""

from mars_control import MarsControlMessage
from mars_hardware import MarsPCB
from time import sleep
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
# logging.disable(logging.INFO)  # Uncomment to disable log messages


# FUNCTIONS
def execute_command():
    while(mc_server.keepalive):
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
        if mc_server.switch_3:
            fwd = True
            logging.info('Forward movement')
        else:
            fwd = False
            logging.info('Reverse movement')
        if mc_server.switch_4:
            mh_server.make_steps(forward=fwd)
            logging.info('Stepper ON')
        else:
            logging.info('Stepper OFF')
            sleep(1)
        if mc_server.button_1:
            mh_server.pickup()
            logging.info('Sample collection')
        else:
            logging.info('No sample collection in progress')
        if mc_server.button_2:
            mh_server.unload()
            logging.info('Unload samples')
        else:
            logging.info('No unload in progress')
        mc_server.batteryv = mh_server.BATTERY.value
        mc_server.lightsen = mh_server.AMBIENT.value
        logging.info('Battery: {bat} Light: {light}'
                     .format(bat=mc_server.batteryv, light=mc_server.lightsen))
        logging.info('-----------')


mc_server = MarsControlMessage(host='192.168.0.27')
mh_server = MarsPCB(steprefresh=1)

logging.info('Testing the inputs and outputs on the rover')
mh_server.check_inputs()
mh_server.check_outputs()
logging.info('Creating the socket')
mc_server.create_socket()

t1 = threading.Thread(target=mc_server.serv)
t2 = threading.Thread(target=execute_command)

t1.start()
t2.start()

t1.join()
t2.join()

mc_server.close()
mh_server.close_gpio_objects()
