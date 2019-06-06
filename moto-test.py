#! python3
# This script is for testing motors on the Pi

from time import sleep
import gpiozero

# gpiozero.Servo(pin, *, initial_value=0, min_pulse_width=1/1000,
# max_pulse_width=2/1000, frame_width=20/1000, pin_factory=None)

# gpiozero.DigitalOutputDevice(pin, *, active_high=True,
# initial_value=False, pin_factory=None)

servotime = 0.5
steptime = 0.01

servo = gpiozero.Servo(23)

en1 = gpiozero.DigitalOutputDevice(0, initial_value=False)
en2 = gpiozero.DigitalOutputDevice(5, initial_value=False)

l1 = gpiozero.DigitalOutputDevice(6)
l2 = gpiozero.DigitalOutputDevice(13)
l3 = gpiozero.DigitalOutputDevice(19)
l4 = gpiozero.DigitalOutputDevice(26)


def stepper_function(stepcount):
    for i in range(1, stepcount):
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


print("Initialized ports, starting servo test...")

for i in range(1, 3):
    sleep(servotime)
    servo.min()
    sleep(servotime)
    servo.mid()
    sleep(servotime)
    servo.max()
    sleep(servotime)

servo.detach()

print("Servo test done. Starting stepper test 1: Nothing is enabled")
stepper_function(100)
print("Starting stepper test 2: Motor 1 enabled")
en1.on()
stepper_function(200)
print("Starting stepper test 3: Motor 2 enabled")
en1.off()
en2.on()
stepper_function(200)
print("Starting stepper test 4: Both motor enabled")
en1.on()
stepper_function(200)

print("Stepper tests done, exiting...")
