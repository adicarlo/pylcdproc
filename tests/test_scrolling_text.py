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

    def test_long(self):
        self.lcd.display("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam vulputate sollicitudin scelerisque. Fusce ex erat, convallis ac arcu ac, auctor volutpat enim. Sed dignissim felis ac neque tristique, id sagittis diam semper. Vestibulum lacinia ante fringilla euismod aliquam. Morbi dapibus tincidunt massa in sollicitudin. Praesent feugiat metus vitae faucibus luctus. Phasellus venenatis tellus vitae lacinia laoreet. Praesent vitae tortor viverra, sodales leo id, malesuada sem. Etiam varius, leo id pretium iaculis, ante tortor interdum dolor, at convallis urna mi sit amet est.")

if __name__ == '__main__':
    unittest.main()
