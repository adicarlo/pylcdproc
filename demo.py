#!/usr/bin/python3

import time
import pylcdproc

def main():
    # lcd = pylcdproc.BaseLCD(appname="test_pylcdproc", host="gw.coo", debug=True)
    # print(lcd.summarize())
    # wid = 'msg1'
    # lcd.widget_add(wid, 'string')
    # lcd.widget_set(wid, 1, 1, 'testing 1 2 3 ...')
    # time.sleep(5)
    # lcd.dispose()

    lcd = pylcdproc.IconFieldLCD(appname="demo", host="gw.coo", debug=True)
    print(lcd.summarize())
    print("filling blocks...")
    lcd.icon_fill('BLOCK_FILLED')
    print("filling checkbox ...")
    lcd.icon_fill('CHECKBOX_ON')

    print("delay...")
    time.sleep(5)

    # FIXME: this one fails (but only if prior icon_fill ran)
    print("running a block...")
    lcd.icon_run('BLOCK_FILLED')

if __name__ == "__main__":
    main()

