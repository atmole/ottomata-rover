# python

"""
On-Board control application for the Mars Rover
"""

from marsrover import MarsControlMessage
from time import sleep
import threading

mc_server = MarsControlMessage()
mc_server.create_socket()
# mc_server.serv()

mc_server.lightsen = 0.78
mc_server.batteryv = 3.21


def exec_command():
    for n in range(10):
        print(n)
        print(mc_server.switch_1)
        print(mc_server.switch_2)
        print(mc_server.potmeter)
        sleep(0.5)


t1 = threading.Thread(target=mc_server.serv)
t2 = threading.Thread(target=exec_command)

t1.start()
t2.start()

t1.join()
t2.join()
sleep(1)
mc_server.close()

# return changing battery voltage
