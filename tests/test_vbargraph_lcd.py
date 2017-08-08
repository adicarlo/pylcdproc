import unittest
import pylcdproc
import lcdtesthelper


class VBargraphLCD(pylcdproc.WidgetFactoryLCD):
    "Example LCD bargraph layout for testing, tons of vbargraphs"
    graphs = []

    def populate_screen(self):
        def popone(x):
            w = self.VBargraph(x=x, y=self.height, length=0)
            self.graphs.append(w)
        self.over_all_cols(popone)

    def set(self, *vallist):
        self.set_list(vallist)

    def set_list(self, vallist):
        for idx, val in enumerate(vallist):
            # print("setting", idx, "to", val)
            self.graphs[idx].update(val)


class TestVBargraphLCD(lcdtesthelper.StaticLCDTest):
    @classmethod
    def instantiateLCD(klass, appname="TestVBargraphLCD",
                       host=lcdtesthelper._default_test_host(), debug=False):
        return VBargraphLCD(appname, host=host, debug=debug)

    def test_base(self):
        self.assertTrue(self.lcd.graphs[0])   # do we have a widget
        self.assertEqual(len(self.lcd.widgets), self.lcd.width)

    def test_widget_ids(self):
        self.assertEqual(self.lcd.graphs[0].wid, "vbar1")
        self.assertEqual(self.lcd.graphs[1].wid, "vbar2")

    def test_single(self):
        "play with first graph"
        self.lcd.graphs[0].update(1)
        self.lcd.graphs[0].update(5)

    def test_list(self):
        "increasing list of bargraphs"
        vals = range(self.lcd.width)
        self.lcd.set_list(vals)

    def test_mountain(self):
        half = int(self.lcd.width / 2)
        up = range(0, half)
        down = range(half, 0, -1)
        self.lcd.set_list(list(up) + list(down))

    def test_value_one(self):
        "Chasing a bug in LCD where value 1 is value 2"
        self.lcd.set_list([0, 1, 2] * int(self.lcd.width / 3))


if __name__ == '__main__':
    unittest.main()
