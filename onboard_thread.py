# python

"""
On-Board control application for the Mars Rover
"""

from marsrover import MarsControlMessage
from time import sleep
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
# logging.disable(logging.INFO)  # Uncomment to disable log messages


# FUNCTIONS
def execute_command():
    while(mc_server.keepalive):
        if mc_server.switch_1:
            logging.info('Left drive enabled')
        else:
            logging.info('Left drive disabled')
        if mc_server.switch_2:
            logging.info('Right drive enabled')
        else:
            logging.info('Right drive disabled')
        sleep(1)


def adc_simulator():
    for n in range(10):
        mc_server.batteryv -= float(n)/87
        mc_server.lightsen += float(n)/42
        sleep(2)


mc_server = MarsControlMessage()
mc_server.create_socket()

# Initial values
mc_server.lightsen = 0.78
mc_server.batteryv = 3.21


t1 = threading.Thread(target=mc_server.serv)
t2 = threading.Thread(target=execute_command)
t3 = threading.Thread(target=adc_simulator)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
sleep(1)
mc_server.close()
