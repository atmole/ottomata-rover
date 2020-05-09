import json


class MarsControlMessage:
    """This class sends control messages based on the input."""

    def __init__(self, switch_1=False, switch_2=False, switch_3=False,
                 switch_4=False, button_1=False, button_2=False, potmeter=0.1):
        self.switch_1 = switch_1
        self.switch_2 = switch_2
        self.switch_3 = switch_3
        self.switch_4 = switch_4
        self.button_1 = button_1
        self.button_2 = button_2
        self.potmeter = potmeter

    def message(self):
        """Returns the stored dictionary."""
        self.control_dictionary = {
            "switch_1": self.switch_1,
            "switch_2": self.switch_2,
            "switch_3": self.switch_3,
            "switch_4": self.switch_4,
            "button_1": self.button_1,
            "button_2": self.button_2,
            "potmeter": self.potmeter
            }
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
        self.json_dictionary = json.loads(self.control_string)
        return self.control_string

    def received(self):
        """Returns a dictionary containing the received command."""
        pass
