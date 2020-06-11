#! python3

"""
Mission Control (remote) application for the Mars Rover
"""

from mars_control import MarsControlMessage
from mars_hardware import MarsPCB
from time import sleep
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
# logging.disable(logging.INFO)

mc_client = MarsControlMessage(host='192.168.0.27')
mh_client = MarsPCB()
mh_client.check_inputs()
mc_client.connect()

while(mc_client.keepalive):
    if mh_client.SWITCH_1.is_pressed:
        mc_client.switch_1 = True
        logging.info('Left drive enabled')
    else:
        mc_client.switch_1 = False
        logging.info('Left drive disabled')
    if mh_client.SWITCH_2.is_pressed:
        mc_client.switch_2 = True
        logging.info('Right drive enabled')
    else:
        mc_client.switch_2 = False
        logging.info('Right drive disabled')
    mc_client.switch_3 = mh_client.SWITCH_3.is_pressed
    mc_client.switch_4 = mh_client.SWITCH_4.is_pressed
    mc_client.button_1 = not round(mh_client.BUTTON1.value)
    mc_client.button_2 = not round(mh_client.BUTTON2.value)
    mc_client.potmeter = mh_client.POTMETR.value*100
    mc_client.keepalive = mh_client.SWITCH_5.is_pressed
    mc_client.send()
    logging.info('Battery Level: {ba}'.format(ba=mc_client.batteryv))
    logging.info('Light Level: {li}'.format(li=mc_client.lightsen))
    sleep(1)

mh_client.close_gpio_objects()
mc_client.close()
