import unittest
from marsrover import MarsControlMessage


class TestMarsControlMessage(unittest.TestCase):

    def setUp(self):
        self.mc_1 = MarsControlMessage(False, False, False, False,
                                       False, False, 0.55)
        self.mc_2 = MarsControlMessage(True, False, True, "three",
                                       True, True, 0.12)
        self.mc_3 = MarsControlMessage(False, False, True, False,
                                       True, True, 1.97)

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
