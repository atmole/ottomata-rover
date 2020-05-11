# python

"""
Mission Control (remote) application for the Mars Rover
"""

from marsrover import MarsControlMessage
from time import sleep

mc_client = MarsControlMessage()
# print(mc_client.message())
mc_client.button_1 = 1
mc_client.switch_2 = 1
mc_client.potmeter = 0.7
mc_client.connect()
for i in range(0, 100):
    mc_client.send()
    sleep(0.001)
mc_client.close()
