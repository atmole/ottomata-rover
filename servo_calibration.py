import gpiozero
from time import sleep

SERVO_1 = gpiozero.Servo(24)
angle = 50
interval = 0.5

print("""
1) This script will prompt you for servo angles. (0%-100%)
2) Then it will set the servo and detach it.
3) This repeats while the value you enter is below 100.
4) 101 starts a sweeping movement with increasing angles.
5) 102 starts a slow and gradual turn from 0 to 100%.
6) 103 is a button press movement.
""")

"""
NOTES
SERVO_1 shall to -99 (full open) to +99 (full closed)
SERVO_2 is shut at 15 and full open at -99
"""


# FUNCTIONS
def servo_sequence(list):
    for a in list:
        print(a)
        SERVO_1.value = a/100
        sleep(interval)


# SCRIPT
while angle < 101:
    angle = int(input("Set servo to: "))
    if angle < 100:
        SERVO_1.value = angle/100
        sleep(interval)
        SERVO_1.detach()
    else:
        pass

angle_list = [0, 10, -10, 20, -20, 0, 40, -40, 0, 80, -80, 0, 99, -99, 0]
button_list = [60, 40, 30, 25, 20, 40, 80]

if angle == 101:
    print("Sweeping...")
    servo_sequence(angle_list)
elif angle == 102:
    print("Gradual turning...")
    for a in range(0, 100, 5):
        print(a)
        SERVO_1.value = a/100
        sleep(interval)
    for a in range(100, 0, -10):
        print(a)
        SERVO_1.value = a/100
        sleep(interval)
elif angle == 103:
    print("Button Press...")
    servo_sequence(button_list)
else:
    print("Exit...")

SERVO_1.detach()
