import unittest
import pylcdproc
import lcdtesthelper

class TestCommandSuccess(lcdtesthelper.BaseLCDTest):
    def test_basic(self):
        self.assertTrue(self.lcd.command_success('output on'))

    def test_bad_command(self):
        with self.assertRaises(pylcdproc.LCDNoSuccessError):
            print("DEBUG:", self.lcd.command_success('noop'))


if __name__ == '__main__':
    unittest.main()

