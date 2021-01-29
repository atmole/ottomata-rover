import gpiozero
from time import sleep


class MarsPCB:
    """Hardware interface of the Mars Rover"""

    def __init__(self, steprefresh=1):
        # Variables
        self.servotime = 0.5
        self.steptime = 0.01            # 100 Hz step frequency
        self.steprefresh = steprefresh  # timespan of stepping sequence [s]
        self.just_length = 24           # justification length

        # Initialization
        self.SERVO_1 = gpiozero.Servo(24)
        self.SERVO_2 = gpiozero.Servo(25)

        self.MOSFET1_G = gpiozero.DigitalOutputDevice(12, initial_value=False)
        self.MOSFET2_G = gpiozero.DigitalOutputDevice(16, initial_value=False)
        self.MOSFET3_G = gpiozero.DigitalOutputDevice(20, initial_value=False)
        self.MOSFET4_G = gpiozero.DigitalOutputDevice(21, initial_value=False)

        self.COIL_1 = gpiozero.DigitalOutputDevice(17, initial_value=False)
        self.COIL_2 = gpiozero.DigitalOutputDevice(27, initial_value=False)
        self.COIL_3 = gpiozero.DigitalOutputDevice(22, initial_value=False)
        self.COIL_4 = gpiozero.DigitalOutputDevice(5,  initial_value=False)

        self.LIGHT = gpiozero.DigitalOutputDevice(13, initial_value=False)
        self.BUZZER = gpiozero.DigitalOutputDevice(6, initial_value=False)

        self.SWITCH_1 = gpiozero.Button(14)
        self.SWITCH_2 = gpiozero.Button(15)
        self.SWITCH_3 = gpiozero.Button(18)
        self.SWITCH_4 = gpiozero.Button(23)
        self.SWITCH_5 = gpiozero.Button(26)  # BCM 26 (Mission Cont Shutdown)
        self.SWITCH_6 = gpiozero.Button(19)  # BCM 19 (Limit switch input)

        self.BATTERY = gpiozero.MCP3008(channel=0)
        self.AMBIENT = gpiozero.MCP3008(channel=1)
        self.BUTTON1 = gpiozero.MCP3008(channel=2)
        self.BUTTON2 = gpiozero.MCP3008(channel=3)
        self.POTMETR = gpiozero.MCP3008(channel=4)
        self.SWITCH_7 = gpiozero.MCP3008(channel=5)  # Spare limit switch input
        self.SWITCH_8 = gpiozero.MCP3008(channel=6)  # Spare limit switch input

        self.COILS_FWD = [self.COIL_1, self.COIL_2, self.COIL_3, self.COIL_4]
        self.COILS_REV = [self.COIL_4, self.COIL_3, self.COIL_2, self.COIL_1]
        self.SWITCHES = [self.SWITCH_1, self.SWITCH_2,
                         self.SWITCH_3, self.SWITCH_4]
        self.MOSFETS = [self.MOSFET1_G, self.MOSFET2_G,
                        self.MOSFET3_G, self.MOSFET4_G]

    def sequence(self):
        """Returns how many times to loop over the coils."""
        return int(self.steprefresh / self.steptime / 4)

    def make_steps(self, forward=True):
        """Loops over the coils for the time specified in steprefresh."""
        if forward:
            direction = self.COILS_FWD
        else:
            direction = self.COILS_REV
        for i in range(1, self.sequence()):
            for coil in direction:
                coil.on()
                sleep(self.steptime)
                coil.off()

    def print_ljust(self, text):
        print(text.ljust(self.just_length-8, '_'), end='')

    def print_rjust(self, text):
        print(text.rjust(8, '_'))

    def check_inputs(self):
        """Checks the input statuses."""
        print("Checking Digital Inputs".center(self.just_length, "="))
        for index, switch in enumerate(self.SWITCHES, start=1):
            self.print_ljust("SWITCH_{i}".format(i=index))
            self.print_rjust(str(switch.is_pressed))
        print("Checking Analog Inputs".center(self.just_length, "="))
        self.print_ljust("BATTERY")
        self.print_rjust("{:.2f}".format(self.BATTERY.value))
        self.print_ljust("AMBIENT")
        self.print_rjust("{:.2f}".format(self.AMBIENT.value))
        self.print_ljust("BUTTON1")
        self.print_rjust(str(not round(self.BUTTON1.value)))
        self.print_ljust("BUTTON2")
        self.print_rjust(str(not round(self.BUTTON2.value)))
        self.print_ljust("POTMETR")
        self.print_rjust("{:.2f}".format(self.POTMETR.value*100))
        self.print_ljust("SWITCH_7")
        self.print_rjust(str(not round(self.SWITCH_7.value)))
        self.print_ljust("SWITCH_8")
        self.print_rjust(str(not round(self.SWITCH_8.value)))

    def close_gpio_objects(self):
        """Closes the Analog Input channels and other GPIO objects."""
        self.BATTERY.close()
        self.AMBIENT.close()
        self.BUTTON1.close()
        self.BUTTON2.close()
        self.POTMETR.close()
        self.SWITCH_7.close()
        self.SWITCH_8.close()
        self.SERVO_1.detach()
        self.SERVO_2.detach()

    def check_outputs(self):
        """Self test for the onboard PCB"""
        for _ in range(4):
            self.LIGHT.on()
            sleep(0.2)
            self.LIGHT.off()
            sleep(0.5)
        self.buzz(4)
        self.MOSFET1_G.on()
        self.MOSFET2_G.on()
        self.make_steps(forward=True)
        self.make_steps(forward=False)
        self.MOSFET2_G.off()
        self.make_steps(forward=True)
        self.MOSFET1_G.off()
        self.MOSFET2_G.on()
        self.make_steps(forward=True)
        self.MOSFET2_G.off()
        self.MOSFET3_G.on()
        while not self.SWITCH_6.value:
            self.make_steps(forward=False)
        self.make_steps(forward=True)
        self.MOSFET3_G.off()
        # self.MOSFET4_G.on()
        # self.make_steps(forward=True)
        # self.make_steps(forward=False)
        # self.MOSFET4_G.off()
        self.SERVO_1.value = 0.98  # rake out
        self.SERVO_2.value = -0.88  # trap door open
        sleep(self.servotime)
        self.SERVO_1.value = -0.99  # rake pulled in
        self.SERVO_2.value = 0.88  # trap door shut
        sleep(self.servotime)
        self.SERVO_1.detach()
        self.SERVO_2.detach()

    def pickup(self):
        """Picks up samples. (Crane and speed must be manually lowered.)"""
        self.buzz(2)
        # Extend the rake completely
        self.SERVO_1.value = -0.98
        sleep(self.servotime)
        self.SERVO_1.detach()
        # Short move forward with both wheels to dig into the balls
        self.MOSFET1_G.on()
        self.MOSFET2_G.on()
        self.make_steps(forward=False)
        self.MOSFET1_G.off()
        self.MOSFET2_G.off()
        # Close the rake to pull in the balls, then move it back to mid
        self.SERVO_1.value = 0.99
        sleep(self.servotime)
        self.SERVO_1.value = -0.99
        sleep(self.servotime)
        self.SERVO_1.detach()
        # Lift the crane until it touches the limit switch
        self.MOSFET3_G.on()
        while not self.SWITCH_6.value:
            self.make_steps(forward=False)
        self.MOSFET3_G.off()
        # add more pullins and extend rake at the top
        # gradual pullin and full pullin at the top

    def unload(self):
        """Unloads container. (Crane and speed must be manually lowered.)"""
        self.buzz(3)
        # Open the trap door on the bottom of the container
        self.SERVO_2.value = -0.88
        sleep(self.servotime)
        # Additional shaky movements to loosen stucked parts
        self.SERVO_1.value = 0.98
        sleep(self.servotime)
        self.SERVO_1.value = -0.88
        self.MOSFET3_G.on()
        while not self.SWITCH_6.value:
            self.make_steps(forward=False)
        self.MOSFET3_G.off()
        # Shut the trap door
        self.SERVO_2.value = 0.88
        sleep(self.servotime)
        self.SERVO_1.detach()
        self.SERVO_2.detach()

    def buzz(self, n):
        """Beep n times."""
        for _ in range(n):
            self.BUZZER.on()
            sleep(0.01)
            self.BUZZER.off()
            sleep(0.2)
