import gpiozero
from time import sleep


class MarsPCB:
    """Hardware interface of the Mars Rover"""

    def __init__(self, steprefresh=1):
        # Variables
        self.servotime = 1
        self.steptime = 0.01   # 100 Hz step frequency
        self.steprefresh = steprefresh  # timespan of stepping sequence [s]
        self.just_length = 25  # justification length

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

        self.IR_LED = gpiozero.DigitalOutputDevice(6,  initial_value=False)
        self.BUZZER = gpiozero.DigitalOutputDevice(13, initial_value=False)
        self.COLORS = gpiozero.DigitalOutputDevice(19, initial_value=False)

        self.SWITCH_1 = gpiozero.Button(14)
        self.SWITCH_2 = gpiozero.Button(15)
        self.SWITCH_3 = gpiozero.Button(18)
        self.SWITCH_4 = gpiozero.Button(23)
        self.SWITCH_5 = gpiozero.Button(26)  # Main board switch

        self.BATTERY = gpiozero.MCP3008(channel=0)
        self.AMBIENT = gpiozero.MCP3008(channel=1)
        self.BUTTON1 = gpiozero.MCP3008(channel=2)
        self.BUTTON2 = gpiozero.MCP3008(channel=3)
        self.POTMETR = gpiozero.MCP3008(channel=4)

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

    def close_gpio_objects(self):
        """Closes the Analog Input channels and other GPIO objects."""
        self.BATTERY.close()
        self.AMBIENT.close()
        self.BUTTON1.close()
        self.BUTTON2.close()
        self.POTMETR.close()
        self.SERVO_1.detach()
        self.SERVO_2.detach()

    def check_outputs(self):
        """Self test for the onboard PCB"""
        self.IR_LED.on()
        self.BUZZER.on()
        self.COLORS.on()
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
        self.make_steps(forward=True)
        self.make_steps(forward=False)
        self.MOSFET3_G.off()
        self.IR_LED.off()
        self.BUZZER.off()
        self.COLORS.off()
        for _ in range(4):
            self.MOSFET4_G.on()
            sleep(0.25)
            self.MOSFET4_G.off()
        self.SERVO_1.value = 0
        self.SERVO_2.value = 0
        sleep(self.servotime)
        self.SERVO_1.value = 1
        self.SERVO_2.value = 1
        sleep(self.servotime)
        self.SERVO_1.value = 0.2
        self.SERVO_2.value = 0.8
        sleep(self.servotime)
        self.SERVO_1.detach()
        self.SERVO_2.detach()

    def pickup(self):
        """Picks up samples."""
        self.MOSFET1_G.off()
        self.MOSFET2_G.off()
        self.SERVO_1.value = 1
        self.MOSFET3_G.on()
        for _ in range(2):
            self.make_steps(forward=True)
        self.SERVO_1.value = 0
        for _ in range(2):
            self.make_steps(forward=False)
        self.MOSFET3_G.off()
        self.SERVO_1.value = 0.3
        self.SERVO_1.detach()

    def unload(self):
        """Unloads sample container."""
        self.MOSFET1_G.off()
        self.MOSFET2_G.off()
        self.SERVO_1.value = 1
        self.MOSFET3_G.on()
        for _ in range(2):
            self.make_steps(forward=False)
        self.SERVO_1.value = 0.4
        for _ in range(3):
            self.make_steps(forward=True)
        self.MOSFET3_G.off()
        self.SERVO_1.value = 1
        self.SERVO_1.detach()
        for _ in range(2):
            self.make_steps(forward=False)
