import unittest
import pylcdproc

class BaseLCDTest(unittest.TestCase):
    lcd = None

    def setUp(self):
        if not self.lcd:
            self.lcd = type(self).instantiateLCD()

    def instantiateLCD(appname="testLCD", host="gw.coo"):
        return pylcdproc.BaseLCD(appname, host=host)

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

class WidgetLCDTest(BaseLCDTest):
    def instantiateLCD(appname="testLCD", host="gw.coo"):
        return pylcdproc.WidgetFactoryLCD(appname, host=host)


