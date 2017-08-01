import unittest
import pylcdproc
import lcdtesthelper

class TestBargraphLCD(lcdtesthelper.BaseLCDTest):
    def instantiateLCD(appname="testScrollingText", host="gw.coo"):
        return pylcdproc.BargraphLCD(appname, host)


if __name__ == '__main__':
    unittest.main()
