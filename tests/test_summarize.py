import pylcdproc
import lcdtesthelper

class TestSummarize(lcdtesthelper.BaseLCDTest):
    def test_summarize(self):
        self.assertEqual(self.lcd.summarize(), "server protocol 0.3, lcd 20x2 chars with 5x8 cells")
