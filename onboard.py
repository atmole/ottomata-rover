#! python3

"""
On-Board control application for the Mars Rover
"""

from marsrover import MarsControlMessage
from time import sleep

mc_server = MarsControlMessage()
# print(type(mc_server))
# print(mc_server.message())
mc_server.create_socket()
mc_server.serv()
print(mc_server.switch_1)
print(mc_server.switch_2)
print(mc_server.potmeter)

sleep(1)
mc_server.close()

# add threading
