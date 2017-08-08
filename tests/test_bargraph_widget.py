import unittest
import lcdtesthelper


class TestBargraphWidget(lcdtesthelper.WidgetLCDTest):
    def test_hbase(self):
        old = len(self.lcd.widgets)
        w = self.lcd.HBargraph(x=1, y=1, length=(self.lcd.width - 1))
        self.assertTrue(w.lcd)
        self.assertEqual(w.wid, "hbar1")
        self.assertEqual(len(self.lcd.widgets), old + 1)

    def test_multiple(self):
        w1 = self.lcd.HBargraph()
        w2 = self.lcd.HBargraph()
        self.assertNotEqual(w1.wid, w2.wid)

    def test_vbase(self):
        old = len(self.lcd.widgets)
        w = self.lcd.VBargraph(x=self.lcd.width, y=self.lcd.height,
                               length=self.lcd.height)
        self.assertTrue(w.lcd)
        self.assertEqual(w.wid, "vbar1")
        self.assertEqual(len(self.lcd.widgets), old + 1)


if __name__ == '__main__':
    unittest.main()
