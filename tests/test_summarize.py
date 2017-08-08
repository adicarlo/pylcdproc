import unittest
import lcdtesthelper


class TestSummarize(lcdtesthelper.BaseLCDTest):
    def test_summarize(self):
        r = r"server protocol 0.3, lcd [0-9x]+ chars with [0-9x]+ cells"
        self.assertRegex(self.lcd.summarize(), r)


if __name__ == '__main__':
    unittest.main()
