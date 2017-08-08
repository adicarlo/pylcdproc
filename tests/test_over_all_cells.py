import unittest
import lcdtesthelper


class TestOverAllCells(lcdtesthelper.BaseLCDTest):
    ctr = 0

    def increment_ctr(self):
        self.ctr += 1
        return self.ctr

    def test_over_all_cells(self):
        self.ctr = 0
        self.lcd.over_all_cells(lambda x, y: self.increment_ctr())
        expected = self.lcd.height * self.lcd.width
        self.assertGreater(expected, 1)
        self.assertEqual(self.ctr, expected)


if __name__ == '__main__':
    unittest.main()
