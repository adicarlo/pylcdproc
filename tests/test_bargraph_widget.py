import unittest
import pylcdproc
import lcdtesthelper

class TestBargraphWidget(lcdtesthelper.WidgetLCDTest):
    def test_base(self):
        w = self.lcd.HBargraph(x=1, y=1, length=self.lcd.width)

if __name__ == '__main__':
    unittest.main()
