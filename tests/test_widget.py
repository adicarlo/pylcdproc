import unittest
import time
import pylcdproc
import lcdtesthelper

class TestStringWidget(lcdtesthelper.BaseLCDTest):
    wid = 'test1'

    def setUp(self):
        super().setUp()
        self.lcd.widget_add(self.wid, 'string')

    def tearDown(self):
        # delaying to show what we did
        # time.sleep(5)
        pass

    def test_basic(self):
        self.lcd.widget_set(self.wid, 1, 1, 'testing123...')

    def test_make(self):
        # make a 2nd widget on the 2nd line
        self.lcd.widget_set(self.wid, 1, 1, 'first line')
        self.lcd.widget_make('test2', 'string', 1, 2, 'second line')

    def test_spaces(self):
        self.lcd.widget_set(self.wid, 1, 1, 'testing 1 2 3')

    def test_quotes(self):
        # FIXME: this test should fail right now
        pass


if __name__ == '__main__':
    unittest.main()
