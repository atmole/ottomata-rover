#! python3
# This script is for testing the Mars Rover 2020

from time import sleep
import gpiozero

# gpiozero.Servo(pin, *, initial_value=0, min_pulse_width=1/1000,
# max_pulse_width=2/1000, frame_width=20/1000, pin_factory=None)

# Variables
servotime = 3
steptime = 0.01

# Initialization
SERVO_1 = gpiozero.Servo(24)
SERVO_2 = gpiozero.Servo(25)


MOSFET1_G = gpiozero.DigitalOutputDevice(12, initial_value=False)
MOSFET2_G = gpiozero.DigitalOutputDevice(16, initial_value=False)
MOSFET3_G = gpiozero.DigitalOutputDevice(20, initial_value=False)
MOSFET4_G = gpiozero.DigitalOutputDevice(21, initial_value=False)

COIL_1 = gpiozero.DigitalOutputDevice(17, initial_value=False)
COIL_2 = gpiozero.DigitalOutputDevice(27, initial_value=False)
COIL_3 = gpiozero.DigitalOutputDevice(22, initial_value=False)
COIL_4 = gpiozero.DigitalOutputDevice(5,  initial_value=False)

IR_LED = gpiozero.DigitalOutputDevice(6,  initial_value=False)
BUZZER = gpiozero.DigitalOutputDevice(13, initial_value=False)
COLORS = gpiozero.DigitalOutputDevice(19, initial_value=False)


SWITCH_1 = gpiozero.Button(14)
SWITCH_2 = gpiozero.Button(15)
SWITCH_3 = gpiozero.Button(18)
SWITCH_4 = gpiozero.Button(23)
SWITCH_5 = gpiozero.Button(26)  # Main board switch

BATTERY = gpiozero.MCP3008(channel=0)
AMBIENT = gpiozero.MCP3008(channel=1)
BUTTON1 = gpiozero.MCP3008(channel=2)
BUTTON2 = gpiozero.MCP3008(channel=3)
POTMETR = gpiozero.MCP3008(channel=4)

COILS_FWD = [COIL_1, COIL_2, COIL_3, COIL_4]
COILS_REV = [COIL_4, COIL_3, COIL_2, COIL_1]
SWITCHES = [SWITCH_1, SWITCH_2, SWITCH_3, SWITCH_4]
MOSFETS = [MOSFET1_G, MOSFET2_G, MOSFET3_G, MOSFET4_G]


# FUNCTIONS
def stepper_fwd(stepcount):
    for i in range(1, stepcount):
        for coil in COILS_FWD:
            coil.on()
            sleep(steptime)
            coil.off()


def stepper_rev(stepcount):
    for i in range(1, stepcount):
        for coil in COILS_REV:
            coil.on()
            sleep(steptime)
            coil.off()


# Power On Self-Test
print("Testing the DIs...")
for index, switch in enumerate(SWITCHES, start=1):
    if switch.is_pressed:
        print("SWITCH " + str(index) + " is on")
    else:
        print("SWITCH " + str(index) + " is off")

print("Testing the ADC...")
for i in range(0, 3):
    print("Battery: " + str('{:.3f}'.format(BATTERY.value * 3.3)))
    print("Amb. light: " + str('{:.3f}'.format(AMBIENT.value)))
    print("Button 1: " + str('{:.3f}'.format(BUTTON1.value)))
    print("Button 2: " + str('{:.3f}'.format(BUTTON2.value)))
    print("Potmeter: " + str('{:.3f}'.format(POTMETR.value)))
    print("-===============================-")
    sleep(2)

BATTERY.close()
AMBIENT.close()
BUTTON1.close()
BUTTON2.close()
POTMETR.close()

print("Testing the outputs...")
IR_LED.on()
BUZZER.on()
COLORS.on()
print("ULN2003 is on")

for index, mosfet in enumerate(MOSFETS, start=1):
    mosfet.on()
    print("MOSFET on: " + str(index))
    sleep(1)
    mosfet.off()
    print("MOSFET off: " + str(index))

IR_LED.off()
BUZZER.off()
COLORS.off()

print("Testing servos...")

while(SWITCH_5.is_pressed):
    sleep(servotime)
    if SWITCH_1.is_pressed:
        print("Servos go: 0.00 / 1.00")
        SERVO_1.value = 0
        SERVO_2.value = 1
    elif SWITCH_2.is_pressed:
        print("Servos go: 0.25 / 0.75")
        SERVO_1.value = 0.25
        SERVO_2.value = 0.75
    elif SWITCH_3.is_pressed:
        print("Servos go: 0.50 / 0.50")
        SERVO_1.value = 0.5
        SERVO_2.value = 0.5
    elif SWITCH_4.is_pressed:
        print("Servos go: 1.00 / 0.00")
        SERVO_1.value = 1
        SERVO_2.value = 0
    else:
        print("Nothing is pressed!")

SERVO_1.detach()
SERVO_2.detach()

print("Turn on SWITCH_4 for the stepper driver test!")
sleep(2)
COLORS.on()

while(SWITCH_4.is_pressed):
    if SWITCH_3.is_pressed:
        if SWITCH_1.is_pressed:
            print("Left Drive going forward")
            MOSFET1_G.on()
        else:
            MOSFET1_G.off()
        if SWITCH_2.is_pressed:
            print("Right Drive going forward")
            MOSFET2_G.on()
        else:
            MOSFET2_G.off()
        stepper_fwd(200)
    else:
        if SWITCH_1.is_pressed:
            print("Left Drive going reverse")
            MOSFET1_G.on()
        else:
            MOSFET1_G.off()
        if SWITCH_2.is_pressed:
            print("Right Drive going reverse")
            MOSFET2_G.on()
        else:
            MOSFET2_G.off()
        stepper_rev(200)
    sleep(1)

MOSFET3_G.on()
stepper_fwd(200)
stepper_rev(200)
MOSFET3_G.off()

print("Tests done, closing the script...")
