import gpiozero


class MarsPCB:
    """Hardware interface of the Mars Rover"""

    def __init__(self):
        # Variables
        self.servotime = 3
        self.steptime = 0.05  # 20 Hz

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
