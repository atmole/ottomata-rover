#! /usr/bin/python3
# 1-Wire DS18B20 Sensors

import os
import logging


class Sensors:
    """
    This class is for reading out the temperature values from the
    DS18B20 Sensors.
    """
    def __init__(self, path='/sys/bus/w1/devices/'):
        self.w1path = path
        logging.basicConfig(level=logging.INFO,
                            format='%(levelname)s - %(message)s')

    def getsensors(self):
        sensor_ls = os.popen('ls ' + self.w1path).read()
        if len(sensor_ls) == 0:
            logging.info('No sensors found.')
        else:
            for s in sensor_ls:
                logging.info(s)
        return sensor_ls

    def gettemp(self, id):
        try:
            # f = open(self.w1path + id + '/' + 'w1_slave', 'r')
            f = open(os.path.join(self.w1path, id, 'w1_slave'), 'r')
        except FileNotFoundError:
            return 99999
        line = f.readline()  # read 1st line
        crc = line.rsplit(' ', 1)
        crc = crc[1].replace('\n', '')
        if crc == 'YES':
            line = f.readline()  # read 2nd line
            mytemp = line.rsplit('t=', 1)
        else:
            mytemp = 99999
        f.close()
        return '{:.2f}'.format(int(mytemp[1])/float(1000))
