# python

"""
Mission Control (remote) application for the Mars Rover
"""

from marsrover import MarsControlMessage
from time import sleep

mc_client = MarsControlMessage()
mc_client.connect()

for _ in range(5):
    command = input('> ')
    if 'q' in command:
        mc_client.switch_1 = 1
    else:
        mc_client.switch_1 = 0

    if 'w' in command:
        mc_client.switch_2 = 1
    else:
        mc_client.switch_2 = 0

    mc_client.send()
    sleep(1)

mc_client.keepalive = False
mc_client.send()
mc_client.close()
