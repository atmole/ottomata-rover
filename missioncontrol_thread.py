# python

"""
Mission Control (remote) application for the Mars Rover
"""

from marsrover import MarsControlMessage
from time import sleep

mc_client = MarsControlMessage()
mc_client.connect()

for _ in range(10):
    command = input('> ')
    if command == 'w':
        mc_client.switch_1 = 1
        mc_client.switch_2 = 1
        mc_client.switch_3 = 0
    elif command == 'a':
        mc_client.switch_1 = 0
        mc_client.switch_2 = 1
        mc_client.switch_3 = 0
    elif command == 's':
        mc_client.switch_1 = 1
        mc_client.switch_2 = 1
        mc_client.switch_3 = 1
    elif command == 'd':
        mc_client.switch_1 = 1
        mc_client.switch_2 = 0
        mc_client.switch_3 = 0
    else:
        mc_client.switch_1 = 0
        mc_client.switch_2 = 0
        mc_client.switch_3 = 0

    mc_client.send()
    sleep(1)

mc_client.close()
