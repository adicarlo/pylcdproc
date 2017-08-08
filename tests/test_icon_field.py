import unittest
import pylcdproc
import lcdtesthelper


class IconFieldTestLCD(pylcdproc.IconFieldLCD, pylcdproc.nMediaPCLCD):
    pass


class TestIconField(lcdtesthelper.StaticLCDTest):

    def instantiateLCD(appname="testIconField",
                       host=lcdtesthelper._default_test_host()):
        return IconFieldTestLCD(appname, host)

    def assert_widget_count(self):
        self.assertEqual(len(self.lcd.widgets),
                         self.lcd.width * self.lcd.height)

    def setUp(self):
        super().setUp()
        self.assert_widget_count()

    def test_init(self):
        "Ensure we have all our widgets setup"
        self.assert_widget_count()

    def test_widget_at(self):
        self.assertEqual(self.lcd.widget_at(1, 20), self.lcd.base + "120")

    def fill_one(self, x, y, icon):
        self.lcd.widget_set(self.lcd.widget_at(x, y), x, y, icon)

    def test_fill_block(self):
        "testing fill_block"
        self.lcd.icon_fill('BLOCK_FILLED')
        self.assert_widget_count()
        # print("trying to fill empty space at 20,1")
        self.fill_one(20, 1, 'CHECKBOX_GRAY')
        # print("didn't work, did it?  This is 19,1")
        self.fill_one(19, 1, 'CHECKBOX_GRAY')
        # print("lets shift 19 to 20...")
        self.lcd.widget_set(self.lcd.widget_at(19, 1), 20, 1, 'CHECKBOX_GRAY')
        # print("delaying...")
        # time.sleep(10)

    def test_fill_illegal(self):
        with self.assertRaises(pylcdproc.LCDHuhError):
            self.lcd.icon_fill('NO_SUCH_ICON')

    def test_icon_run(self):
        self.lcd.icon_run('CHECKBOX_GRAY')

    def test_known_icons(self):
        for idx, icon in enumerate(self.lcd.known_icons):
            self.fill_one(idx + 1, 2, icon)


if __name__ == '__main__':
    unittest.main()
