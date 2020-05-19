import unittest
from marsrover import MarsControlMessage


class TestMarsControlMessage(unittest.TestCase):

    def setUp(self):
        self.mc_1 = MarsControlMessage()
        self.mc_1.switch_1 = False
        self.mc_1.switch_2 = False
        self.mc_1.switch_3 = False
        self.mc_1.switch_4 = False
        self.mc_1.button_1 = False
        self.mc_1.button_2 = False
        self.mc_1.potmeter = 0.55

        self.mc_2 = MarsControlMessage()
        self.mc_2.switch_1 = True
        self.mc_2.switch_2 = False
        self.mc_2.switch_3 = True
        self.mc_2.switch_4 = "three"
        self.mc_2.button_1 = False
        self.mc_2.button_2 = False
        self.mc_2.potmeter = 0.59

        self.mc_3 = MarsControlMessage()
        self.mc_3.switch_1 = False
        self.mc_3.switch_2 = False
        self.mc_3.switch_3 = False
        self.mc_3.switch_4 = False
        self.mc_3.button_1 = True
        self.mc_3.button_2 = False
        self.mc_3.potmeter = 1.97

    def test_message(self):
        self.assertEqual(self.mc_1.message(),
                         '{"switch_1": false, "switch_2": false, ' +
                         '"switch_3": false, "switch_4": false, ' +
                         '"button_1": false, "button_2": false, ' +
                         '"potmeter": 0.55}')
        self.assertRaises(ValueError, self.mc_2.message)
        self.assertRaises(ValueError, self.mc_3.message)

    def tearDown(self):
        pass


# if __name__ == '__main__':
#    unittest.main()
