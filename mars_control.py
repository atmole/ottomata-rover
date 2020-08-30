import json
import socket
import logging


class MarsControlMessage:
    """Handles control and diagnostic messages."""

    def __init__(self, host='127.0.0.1', port=50007):
        self.switch_1 = False  # left drive
        self.switch_2 = False  # right drive
        self.switch_3 = False  # forward move if True (rewerse otherwise)
        self.switch_4 = False  # automatic or manual pickup / unload
        self.button_1 = False  # start sample pickup
        self.button_2 = False  # start sample unload
        self.potmeter = 50     # speed
        self.batteryv = 0.0    # battery voltage
        self.lightsen = 0.0    # light sensor
        self.keepalive = True  # keeps the while loop alive
        self.host = host       # host ip address
        self.port = port       # host port
        self.sock = socket.socket()

    def create_socket(self):
        """Creates a server socket and listens for connections."""
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        logging.info('Connected: {a}'.format(a=addr))

    def serv(self):
        """Receives data from the client, replies with diagnostic msg."""
        while True:
            control_string = self.conn.recv(256)
            if not control_string:
                break
            self.update_values(control_string)
            # reply with a diagnostic message
            self.conn.sendall(bytes(self.diagnose(), 'utf-8'))

    def connect(self):
        """Connects to the server."""
        self.sock.connect((self.host, self.port))

    def send(self):
        """Sends the control message to the server, receives diagnostics."""
        self.sock.sendall(bytes(self.control(), 'utf-8'))
        data = self.sock.recv(256)
        diagnostic_dictionary = json.loads(data)
        self.batteryv = diagnostic_dictionary['batteryv']
        self.lightsen = diagnostic_dictionary['lightsen']

    def close(self):
        """Closes the socket."""
        self.sock.close()

    def control(self):
        """Returns an up to date control message string."""
        self.control_dictionary = {
            "switch_1": self.switch_1,
            "switch_2": self.switch_2,
            "switch_3": self.switch_3,
            "switch_4": self.switch_4,
            "button_1": self.button_1,
            "button_2": self.button_2,
            "potmeter": self.potmeter,
            "keepalive": self.keepalive
            }
        # error handling
        for key, value in self.control_dictionary.items():
            if key[0:6] in ["switch", "button", "keepal"]:
                if value in [True, False]:
                    pass
                else:
                    raise ValueError(value, 'is not BOOL')
            elif key == "potmeter":
                if value <= 101 and value > 0:
                    pass
                else:
                    raise ValueError(value, 'is not between 0 and 100.')
            else:
                raise KeyError(key, 'This key should not be here.')
        self.control_string = json.dumps(self.control_dictionary)
        return self.control_string

    def diagnose(self):
        """Returns the diagnostic message string."""
        self.diagnostic_dictionary = {
            "batteryv": "{:.2f}".format(self.batteryv),
            "lightsen": "{:.2f}".format(self.lightsen)
            }
        self.diagnostic_string = json.dumps(self.diagnostic_dictionary)
        return self.diagnostic_string

    def update_values(self, control_string):
        """Updates the values in the object based on the argument string."""
        self.json_dictionary = json.loads(control_string)
        # pprint.pprint(self.json_dictionary)
        self.switch_1 = self.json_dictionary['switch_1']
        self.switch_2 = self.json_dictionary['switch_2']
        self.switch_3 = self.json_dictionary['switch_3']
        self.switch_4 = self.json_dictionary['switch_4']
        self.button_1 = self.json_dictionary['button_1']
        self.button_2 = self.json_dictionary['button_2']
        self.potmeter = self.json_dictionary['potmeter']
        self.keepalive = self.json_dictionary['keepalive']
