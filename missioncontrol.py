# python

"""
Mission Control (remote) application for the Mars Rover
"""

from marsrover import MarsControlMessage
from time import sleep

mc_client = MarsControlMessage()
mc_client.connect()

mc_client.button_1 = 0
mc_client.button_2 = 0
mc_client.switch_1 = 1
mc_client.switch_2 = 1
mc_client.switch_3 = 0
mc_client.switch_4 = 1
mc_client.potmeter = 0.2

mc_client.send()
sleep(1)

mc_client.button_1 = 1
mc_client.button_2 = 0
mc_client.switch_1 = 1
mc_client.switch_2 = 0
mc_client.switch_3 = 1
mc_client.switch_4 = 1
mc_client.potmeter = 0.4

mc_client.send()
mc_client.close()

#  add threading for control input
