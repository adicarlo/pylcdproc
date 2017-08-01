#!/usr/bin/python3

import time
import pylcdproc

def demo_icons():
    lcd = pylcdproc.IconFieldLCD(appname="demo", host="gw.coo", debug=True)
    print(lcd.summarize())
    print("filling blocks...")
    lcd.icon_fill('BLOCK_FILLED')
    print("filling checkbox ...")
    lcd.icon_fill('CHECKBOX_ON')
    print("running a block...")
    lcd.icon_run('BLOCK_FILLED', 'HEART_OPEN')

def main():
    demo_icons()

if __name__ == "__main__":
    main()

