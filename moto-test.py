#! python3
# This script is for testing motors on the Pi

from time import sleep
import gpiozero

# gpiozero.Servo(pin, *, initial_value=0, min_pulse_width=1/1000,
# max_pulse_width=2/1000, frame_width=20/1000, pin_factory=None)

# gpiozero.DigitalOutputDevice(pin, *, active_high=True,
# initial_value=False, pin_factory=None)

servotime = 1
steptime = 0.1

servo = gpiozero.Servo(14)

en = gpiozero.DigitalOutputDevice(5, active_high=False, initial_value=True)

l1 = gpiozero.DigitalOutputDevice(6, active_high=False, initial_value=True)
l2 = gpiozero.DigitalOutputDevice(13, active_high=False, initial_value=True)
l3 = gpiozero.DigitalOutputDevice(19, active_high=False, initial_value=True)
l4 = gpiozero.DigitalOutputDevice(26, active_high=False, initial_value=True)

print("initialized ports, start servo test...")

for i in range(1, 3):
    sleep(servotime)
    servo.min()
    sleep(servotime)
    servo.mid()
    sleep(servotime)
    servo.max()
    sleep(servotime)

servo.detach()

print("servo test done, stepper test...")

en.on()

for i in range(1, 10):
    l1.on()
    sleep(steptime)
    l1.off()
    l2.on()
    sleep(steptime)
    l2.off()
    l3.on()
    sleep(steptime)
    l3.off()
    l4.on()
    sleep(steptime)
    l4.off()

print("stepper test done, exit...")
