import unittest
import pylcdproc
import lcdtesthelper

class TestSetup(lcdtesthelper.BaseLCDTest):
    def test_setup_size(self):
        self.assertEqual(self.lcd.width, 20)
        self.assertEqual(self.lcd.height, 2)

    def test_setup_cell_size(self):
        self.assertEqual(self.lcd.cell_width, 5)
        self.assertEqual(self.lcd.cell_height, 8)

    def test_functional_setup(self):
        self.assertTrue(self.lcd.setup(b"connect LCDproc 0.5.7 protocol 0.3 lcd wid 20 hgt 2 cellwid 5 cellhgt 8\n"))


if __name__ == '__main__':
    unittest.main()

