import unittest
import time
import pylcdproc
import os


def _default_test_host(host=None):
    """
    Default host to connect to.
    """
    return(host or os.environ.get('LCD_TEST_HOST') or 'localhost')


class BaseLCDTest(unittest.TestCase):
    """
    Create a linkage between a class of TestCases and LCD screens.
    """
    lcd = None

    def setUp(self):
        if not self.lcd:
            self.lcd = type(self).instantiateLCD()

    def instantiateLCD(appname="testLCD", host=None):
        return pylcdproc.BaseLCD(appname, host=_default_test_host(host))

    def hold(self, sleep_secs=30):
        print("waiting for", sleep_secs, "seconds")
        time.sleep(sleep_secs)


class StaticLCDTest(BaseLCDTest):
    """
    Variation on BaseLCDTest such that the LCD is shared for each test
    in the class.
    """

    @classmethod
    def setUpClass(cls):
        cls.lcd = cls.instantiateLCD()

    @classmethod
    def tearDownClass(cls):
        cls.lcd.dispose()

    def setUp(self):
        if not self.lcd:
            self.lcd = type(self).lcd

    def tearDown(self):
        pass


class WidgetLCDTest(BaseLCDTest):
    def instantiateLCD(appname="testLCD", host=None):
        return pylcdproc.WidgetFactoryLCD(appname, host=_default_test_host(host))
