import unittest
import pylcdproc
import lcdtesthelper
import time

class HBargraphLCD(pylcdproc.WidgetFactoryLCD):
    "Example LCD bargraph layout for testing, single large hbargraph"
    graph = None

    def populate_screen(self):
        self.graph = self.HBargraph(1, 1, 0)

    def display(self, value):
        self.graph.update(value)


class TestHBargraphLCD(lcdtesthelper.StaticLCDTest):
    max_width = None

    @classmethod
    def instantiateLCD(klass, appname="testScrollingText", host="gw.coo", debug=True):
        return HBargraphLCD(appname, host)

    def setUp(self):
        super().setUp()
        self.max_width = self.lcd.width * self.lcd.cell_width

    def test_base(self):
        "some basic assertions"
        self.assertTrue(self.lcd.graph)   # do we have a widget
        self.assertEqual(len(self.lcd.widgets), 1)

    def test_up(self):
        "run from zero to max"
        for i in range(0, self.max_width):
            self.lcd.display(i)

    def test_down(self):
        "run max to zero"
        for i in range(self.max_width, 0, -1):
            self.lcd.display(i)


if __name__ == '__main__':
    unittest.main()
