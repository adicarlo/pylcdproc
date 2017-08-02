import unittest
import pylcdproc
import lcdtesthelper
import time

class VBargraphLCD(pylcdproc.WidgetFactoryLCD):
    "Example LCD bargraph layout for testing, tons of vbargraphs"
    graphs = []

    def populate_screen(self):
        def popone(x):
            w = self.VBargraph(x=x, y=self.height, length=0)
            self.graphs.append(w)
        self.over_all_cols(popone)

    def set(self, *vallist):
        for idx, val in enumerate(vallist):
            self.graphs[idx].update(val)



class TestVBargraphLCD(lcdtesthelper.StaticLCDTest):
    @classmethod
    def instantiateLCD(klass, appname="TestVBargraphLCD", host="gw.coo", debug=False):
        return VBargraphLCD(appname, host=host, debug=debug)

    def test_base(self):
        self.assertTrue(self.lcd.graphs[0])   # do we have a widget
        self.assertEqual(len(self.lcd.widgets), self.lcd.width)

    def test_widget_ids(self):
        self.assertEqual(self.lcd.graphs[0].wid, "vbar1")
        self.assertEqual(self.lcd.graphs[1].wid, "vbar2")

    def test_single(self):
        "play with first graph"
        print('setting to one...')
        self.lcd.graphs[0].update(1)
        print('setting to five...')
        self.lcd.graphs[0].update(5)

    def test_list(self):
        "increasing list of bargraphs"
        vals = range(self.lcd.width)
        self.lcd.set(*vals)
        time.sleep(5)

if __name__ == '__main__':
    unittest.main()
