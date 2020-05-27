# python

"""
On-Board control application for the Mars Rover
"""

from marsrover import MarsControlMessage
from time import sleep
import threading

mc_server = MarsControlMessage()
mc_server.create_socket()

mc_server.lightsen = 0.78
mc_server.batteryv = 3.21


def exec_command():
    for n in range(10):
        mc_server.batteryv -= float(n)/87
        mc_server.lightsen += float(n)/42
        sleep(1)


t1 = threading.Thread(target=mc_server.serv)
t2 = threading.Thread(target=exec_command)

t1.start()
t2.start()

t1.join()
t2.join()
sleep(1)
mc_server.close()
