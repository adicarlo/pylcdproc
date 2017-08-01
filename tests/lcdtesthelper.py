import unittest
import pylcdproc

class BaseLCDTest(unittest.TestCase):
    lcd = None

    def instantiateLCD(appname="testLCD", host="gw.coo"):
        return pylcdproc.BaseLCD(appname, host=host)

    def setUp(self):
        if not self.lcd:
            self.lcd = type(self).instantiateLCD()

class StaticLCDTest(BaseLCDTest):
    "variation on BaseLCDTest such that the LCD is shared for each test in the class"

    @classmethod
    def setUpClass(cls):
        cls.lcd = cls.instantiateLCD()

    def setUp(self):
        if not self.lcd:
            self.lcd = type(self).lcd

    def tearDown(self):
        pass
