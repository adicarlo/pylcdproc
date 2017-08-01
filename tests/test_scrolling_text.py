import unittest
import time
import pylcdproc
import lcdtesthelper

class TestScrollingText(lcdtesthelper.StaticLCDTest):
    def instantiateLCD(appname="testScrollingText", host="gw.coo"):
        return pylcdproc.ScrollingTextLCD(appname, host)

    def test_base(self):
        "Should have one widget per line"
        self.assertEqual(len(self.lcd.widgets), self.lcd.height)

    def test_text(self):
        self.lcd.display("short msg")
        self.lcd.display("longer message is known to be rather long")


if __name__ == '__main__':
    unittest.main()
