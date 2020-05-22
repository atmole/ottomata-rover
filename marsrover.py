import json
import socket
import pprint


class MarsControlMessage:
    """This class handles control messages."""

    def __init__(self, host='127.0.0.1', port=50007):
        self.switch_1 = False
        self.switch_2 = False
        self.switch_3 = False
        self.switch_4 = False
        self.button_1 = False
        self.button_2 = False
        self.potmeter = 0.1
        self.batteryv = 0.0
        self.lightsen = 0.0
        self.host = host
        self.port = port
        self.sock = socket.socket()

    def create_socket(self):
        """Creates a socket and listens for connection."""
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.conn, addr = self.sock.accept()
        print("Connected: ", addr)

    def serv(self):
        """Receives data from the client."""
        while True:
            control_string = self.conn.recv(256)
            print(control_string)
            if not control_string:
                break
            self.update_values(control_string)
            # send diagnostic message
            self.conn.sendall(bytes(self.diagnose(), 'utf-8'))

    def connect(self):
        """Connects to the server."""
        self.sock.connect((self.host, self.port))

    def send(self):
        """Sends the control message to the server."""
        self.sock.sendall(bytes(self.control(), 'utf-8'))
        data = self.sock.recv(256)
        print(data)

    def close(self):
        self.sock.close()

    def control(self):
        """Returns the control message string."""
        self.control_dictionary = {
            "switch_1": self.switch_1,
            "switch_2": self.switch_2,
            "switch_3": self.switch_3,
            "switch_4": self.switch_4,
            "button_1": self.button_1,
            "button_2": self.button_2,
            "potmeter": self.potmeter
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
            else:
                raise KeyError(key, 'This key should not be here.')
        self.control_string = json.dumps(self.control_dictionary)
        return self.control_string

    def diagnose(self):
        """Returns the diagnostic message string."""
        self.diagnostic_dictionary = {
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
