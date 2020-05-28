import json
import socket
import pprint


class MarsControlMessage:
    """Handles control and diagnostic messages."""

    def __init__(self, host='127.0.0.1', port=50007):
        self.switch_1 = False  # enable left drive
        self.switch_2 = False  # enable right drive
        self.switch_3 = False  # enable forward move (rewerse otherwise)
        self.switch_4 = False  # enable stepper
        self.button_1 = False  # start pickup sequence
        self.button_2 = False  # enable flashlight
        self.potmeter = 0.1    # set speed
        self.batteryv = 0.0
        self.lightsen = 0.0
        self.keepalive = True  # keeps the while loop alive
        self.host = host
        self.port = port
        self.sock = socket.socket()

    def create_socket(self):
        """Creates a server socket and listens for connections."""
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        print("Connected: ", addr)

    def serv(self):
        """Receives data from the client, replies with diagnostic msg."""
        while True:
            control_string = self.conn.recv(256)
            # print(control_string)
            if not control_string:
                break
            self.update_values(control_string)
            # send diagnostic message
            self.conn.sendall(bytes(self.diagnose(), 'utf-8'))

    def connect(self):
        """Connects to the server."""
        self.sock.connect((self.host, self.port))

    def send(self):
        """Sends the control message to the server, receives diagnostis."""
        self.sock.sendall(bytes(self.control(), 'utf-8'))
        data = self.sock.recv(256)
        self.diagnostic_dictionary = json.loads(data)
        pprint.pprint(self.diagnostic_dictionary)

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
            if key[0:6] in ["switch", "button"]:
                if value in [True, False]:
                    pass
                else:
                    raise ValueError(value, 'is not BOOL')
            elif key == "potmeter":
                if value < 1 and value > 0:
                    pass
                else:
                    raise ValueError(value, 'is not between 0 and 1.')
            elif key == "keepalive":
                pass
            else:
                raise KeyError(key, 'This key should not be here.')
        self.control_string = json.dumps(self.control_dictionary)
        return self.control_string

    def diagnose(self):
        """Returns the diagnostic message string."""
        self.diagnostic_dictionary = {
            # format the floats to make them shorter
            "batteryv": self.batteryv,
            "lightsen": self.lightsen
            }
        self.diagnostic_string = json.dumps(self.diagnostic_dictionary)
        return self.diagnostic_string

    def update_values(self, control_string):
        """Updates the values in the object based on the argument string."""
        self.json_dictionary = json.loads(control_string)
        pprint.pprint(self.json_dictionary)
        self.switch_1 = self.json_dictionary['switch_1']
        self.switch_2 = self.json_dictionary['switch_2']
        self.switch_3 = self.json_dictionary['switch_3']
        self.switch_4 = self.json_dictionary['switch_4']
        self.button_1 = self.json_dictionary['button_1']
        self.button_2 = self.json_dictionary['button_2']
        self.potmeter = self.json_dictionary['potmeter']
        self.keepalive = self.json_dictionary['keepalive']
