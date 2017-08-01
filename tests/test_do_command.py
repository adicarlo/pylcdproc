import unittest
import pylcdproc
import lcdtesthelper

class TestDoCommand(lcdtesthelper.BaseLCDTest):
    def test_hello(self):
        self.assertTrue(self.lcd.do_command('hello'))

    def test_noop(self):
        self.assertEqual(self.lcd.do_command('noop'), b"noop complete\n")

    def test_bad_command(self):
        with self.assertRaises(pylcdproc.LCDHuhError):
            print("DEBUG:", self.lcd.do_command('nosuchcommand'))

if __name__ == '__main__':
    unittest.main()

