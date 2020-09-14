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

msg_mc = MarsControlMessage(host='192.168.2.10')
hw_mc = MarsPCB()
hw_mc.check_inputs()
sleep(2)
msg_mc.connect()

while(msg_mc.keepalive):
    if hw_mc.SWITCH_1.is_pressed:  # switches are inverted on the layout
        msg_mc.switch_1 = False
        logging.info('Left drive disabled')
    else:
        msg_mc.switch_1 = True
        logging.info('Left drive enabled')
    if hw_mc.SWITCH_2.is_pressed:
        msg_mc.switch_2 = False
        logging.info('Right drive disabled')
    else:
        msg_mc.switch_2 = True
        logging.info('Right drive enabled')
    msg_mc.switch_3 = hw_mc.SWITCH_3.is_pressed
    msg_mc.switch_4 = not hw_mc.SWITCH_4.is_pressed
    msg_mc.button_1 = not round(hw_mc.BUTTON1.value)
    msg_mc.button_2 = not round(hw_mc.BUTTON2.value)
    msg_mc.potmeter = hw_mc.POTMETR.value*100
    msg_mc.keepalive = hw_mc.SWITCH_5.is_pressed
    msg_mc.send()  # returns with diagnostic messages from the rover
    # Calculate battery percentage (5.2V - 8.4V)
    battery_percentage = int((float(msg_mc.batteryv) - 5.2) / 3.2 * 100)
    logging.info('Battery Voltage: {ba} V; Battery Level: {bp} %'
                 .format(ba=msg_mc.batteryv, bp=battery_percentage))
    logging.info('Light Level: {li}'.format(li=msg_mc.lightsen))
    logging.info('Potmeter: {pot}'.format(pot=msg_mc.potmeter))
    logging.info('loop end'.center(20, '-'))
    sleep(0.5)

hw_mc.close_gpio_objects()
msg_mc.close()
