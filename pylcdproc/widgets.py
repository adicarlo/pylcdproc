import pylcdproc

##
## widgets
##
class LCDWidget:
    """
Base class for lcdproc widgets.  Always associated with an LCD.
    """
    lcd         = None
    widget_type = None
    wid         = None
    def __init__(self, lcd):
        self.lcd = lcd
        self.set_wid()
        self.lcd.widget_add(self.wid, self.widget_type)

    def set_wid(self):
        self.wid = self.widget_type + str(self.lcd.ctr)
        self.lcd.incr_ctr()
        return self.wid

    def draw(self):
        "Simply draw the widget, using current settings"
        raise NotImplementedError

    def set(self, *args):
        "Set the widget parameters and draw the widget"
        raise NotImplementedError


class BargraphWidget(LCDWidget):
    widget_type = None          # override in subclass
    x           = None
    y           = None
    length      = None

    def __init__(self, lcd, x=1, y=1, length=1):
        super().__init__(lcd)
        (self.x, self.y, self.length) = (x, y, length)

    def draw(self):
        self.lcd.widget_set(self.wid, self.x, self.y, self.length)

    def set(self, x, y, length):
        (self.x, self.y, self.length) = (x, y, length)
        self.lcd.widget_set(self.wid, x, y, length)

    def update(self, length):
        self.length = length
        self.lcd.widget_set(self.wid, self.x, self.y, length)


class HBargraph(BargraphWidget):
    widget_type = 'hbar'


class VBargraph(BargraphWidget):
    widget_type = 'vbar'


class Scroller(LCDWidget):
    widget_type = 'scroller'
    left = top = right = bottom = direction = speed = text = None

    # FIXME: use *vargs here to tramp stuff through?
    def __init__(self, lcd, left=1, top=1, right=None, bottom=None,
                 direction='h', speed=1, text=None):
        super().__init__(lcd)
        self.set(left, top, right, bottom, direction, speed, text)

    def draw(self):
        self.lcd.widget_set(self.wid, self.left, self.top, self.right, self.bottom,
                            self.direction, self.speed, self.text)

    def set_default_right(self):
        "Default to the right margin"
        self.right = self.lcd.width

    def set_default_bottom(self):
        "Default to one line"
        self.bottom = self.top

    def set(self, left, top, right=None, bottom=None, direction=None,
            speed=None, text=None):
        (self.left, self.top, self.direction, self.speed) = \
                (left, top, direction, speed)
        if right is None and self.right is None:
            self.set_default_right()
        if bottom is None and self.bottom is None:
            self.set_default_bottom()
        self.draw()

    def update(self, text):
        self.text = text
        self.draw()


class WidgetFactoryLCD(pylcdproc.BaseLCD):
    # widget counter
    ctr = 1

    def incr_ctr(self):
        self.ctr += 1

    def HBargraph(self, x=None, y=None, length=None):
        return HBargraph(self, x, y, length)

    def VBargraph(self, x=None, y=None, length=None):
        return VBargraph(self, x, y, length)

    def Scroller(self, left, top, right=None, bottom=None):
        return Scroller(self, left, top, right, bottom)


