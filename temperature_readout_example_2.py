#! /usr/bin/python3

import ds18b20

temp_sens = ds18b20.Sensors()

sensor_list = temp_sens.getsensors()

for s in sensor_list:
    print(temp_sens.gettemp())
