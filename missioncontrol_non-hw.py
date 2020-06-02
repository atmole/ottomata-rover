#! python3

"""
Mission Control (remote) application for the Mars Rover
"""

from mars_control import MarsControlMessage
from time import sleep

mc_client = MarsControlMessage()
mc_client.connect()


def set_from_kbd(key_true, key_false, command, prev):
    if key_true in command:
        enabler = True
    elif key_false in command:
        enabler = False
    else:
        enabler = prev
    return enabler


# Control the rover with the keyboard
while mc_client.keepalive:
    command = input('> ')
    mc_client.switch_1 = set_from_kbd('q', 'a', command, mc_client.switch_1)
    mc_client.switch_2 = set_from_kbd('w', 's', command, mc_client.switch_2)
    mc_client.switch_3 = set_from_kbd('e', 'd', command, mc_client.switch_3)
    mc_client.switch_4 = set_from_kbd('r', 'f', command, mc_client.switch_4)
    mc_client.button_1 = set_from_kbd('t', 'g', command, mc_client.button_1)
    mc_client.button_2 = set_from_kbd('z', 'h', command, mc_client.button_2)
    mc_client.keepalive = set_from_kbd('c', 'x', command, mc_client.keepalive)
    mc_client.send()
    sleep(1)


mc_client.close()
