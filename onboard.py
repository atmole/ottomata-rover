# python

"""
On-Board control application for the Mars Rover
"""

from marsrover import MarsControlMessage
from time import sleep

mc_server = MarsControlMessage()
# print(mc_server.message())
mc_server.host()
mc_server.serv()
sleep(1)
mc_server.close()
