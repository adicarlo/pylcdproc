import telnetlib
import re


# custom exceptions
class LCDError(RuntimeError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)


class LCDCommandError(RuntimeError):
    def __init__(self, message, command='unknown command'):
        self.message = message
        self.command = command

    def __str__(self):
        return repr(self.message) + ", command: " + repr(self.command)


class LCDLogicError(LCDError): pass
class LCDGarbledSetup(LCDError): pass
class LCDHuhError(LCDCommandError): pass
class LCDProtocolError(LCDCommandError): pass
class LCDNoSuccessError(LCDCommandError): pass


class BaseLCD:
    """
Very basic interface to LCDd via telnet.  Assumes we only have one screen!
    """
    tn          = None
    protocol    = None
    reqproto    = ['0.3']                # list of supported protocols
    version     = None
    width       = None
    height      = None
    cell_width  = None
    cell_height = None
    widgets     = []
    debug       = False
    # all known icons from widget.c, some models will support only some
    known_icons = [ 'BLOCK_FILLED', 'CHECKBOX_GRAY', 'HEART_OPEN',
        'HEART_FILLED', 'ARROW_UP', 'ARROW_DOWN', 'ARROW_LEFT', 'ARROW_RIGHT',
        'CHECKBOX_OFF', 'CHECKBOX_ON', 'SELECTOR_AT_LEFT', 'SELECTOR_AT_RIGHT',
        'ELLIPSIS', 'STOP', 'PAUSE', 'PLAY', 'PLAYR', 'FF', 'FR', 'NEXT',
        'PREV', 'REC' ]

    def __init__(self, appname, host='localhost', port=13666,
                 debug=False, priority='foreground'):
        assert isinstance(appname, str), "appname must be a string"
        self.debug = debug
        self.tn = telnetlib.Telnet(host, port, 5)
        # the response to hello
        greeting = self.do_command('hello')
        self.setup(greeting)
        # setup application name
        self.appname = appname
        self.do_command("client_set -name " + appname)
        # setup screen, always just called 's'
        self.do_command("screen_add s")
        self.do_command("screen_set s -priority " + priority)
        self.do_command("screen_set s -heartbeat off")
        self.do_command("screen_set s -cursor off")
        self.flush_read()
        self.widgets = []
        self.populate_screen()

    def verbose(self, msg):
        if self.debug:
            print("DEBUG:", msg)

    def readline(self):
        result = self.tn.read_until(b"\n")
        self.verbose("<< " + str(result))
        return result

    def writeline(self, line):
        self.verbose(">> " + line)
        return self.tn.write(line.encode('ascii') + b"\n")

    def read_line_ignoring_noise(self):
        result = self.tn.read_until(b"\n")
        if result == b"listen s\n" or result == b"ignore s\n":
            result = self.tn.read_until(b"\n")
        self.verbose("<< " + str(result))
        return result

    def flush_read(self):
        data = ""
        read = self.tn.read_lazy()
        while read != b'':
            data += read
            read = self.tn.read_lazy()
        if data:
            self.verbose("<{ " + str(data))
        return data

    def do_command(self, command):
        # send command and check result
        self.writeline(command)
        result = self.read_line_ignoring_noise()
        if not result.startswith(b"huh? "):
            return result
        else:
            raise LCDHuhError(result, command)

    def command_success(self, command):
        result = self.do_command(command)
        if result == b"success\n":
            return True
        else:
            raise LCDNoSuccessError(result, command)

    def setup(self, setupstring):
        "Making use of the result of 'hello', check protocol and populate LCD attributes"
        # setup string might look like this:
        #  connect LCDproc 0.5.7 protocol 0.3 lcd wid 20 hgt 2 cellwid 5 cellhgt 8
        m = re.match(r"b'connect LCDproc ([0-9.]+) protocol ([0-9.]+) lcd (.*)'", str(setupstring))
        if m:
            (self.version, self.protocol, remainder) = m.groups()
            if self.protocol in self.reqproto:
                # get lcd-specific settings, I'm not sure this is always the same
                m = re.match(r"wid ([0-9]+) hgt ([0-9]+) cellwid ([0-9]+) cellhgt ([0-9]+)", remainder)
                if m:
                    (self.width, self.height, self.cell_width, self.cell_height) = \
                    list(map(lambda x: int(x), m.groups()))
                return True
            else:
                raise LCDProtocolError(self.protocol)
        else:
            print("failed to understand LCD 'hello' response, crazy")
            raise LCDGarbledSetup(setupstring)

    def populate_screen(self):
        "Populate the newly created screen, if necessary."
        pass

    def summarize(self):
        return 'server protocol ' + self.protocol + ', ' + \
          'lcd ' + str(self.width) + 'x' + str(self.height) + ' chars with ' + \
          str(self.cell_width) + 'x' + str(self.cell_height) + ' cells'

    def widget_add(self, wid, wtype):
        "Add a widget, providing its ID and type"
        self.command_success('widget_add s ' + wid + ' ' + wtype)
        self.widgets.append(wid)
        return wid

    def widget_set(self, wid, *widget_args):
        cmd = 'widget_set s ' + wid + ' "' + '" "'.join(map(lambda x: str(x), widget_args)) + '"'
        # print("DEBUG", cmd)
        self.command_success(cmd)

    def widget_make(self, wid, wtype, *widget_args):
        self.widget_add(wid, wtype)
        self.widget_set(wid, *widget_args)

    def widget_del(self, wid):
        print("DEBUG deleting widget", wid)
        self.command_success('widget_del s ' + wid)

    def dispose_widgets(self):
        map(lambda x: self.widget_del(x), self.widgets)

    def over_all_cells(self, func):
        """
        Run a function over all cells, starting with row 1, left to
        right, top to bottom.  Indexed at 1.
        """
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                func(x, y)

    def over_all_cols(self, func):
        "Run a function over all columns in a screen, 1-indexed."
        for x in range(1, self.width + 1):
            func(x)

    def over_all_rows(self, func):
        "Run a function over all rows in a screen, 1-indexed."
        for y in range(1, self.height + 1):
            func(y)

    def dispose(self):
        # we could careful delete widgets and the screen, but its easier to
        # just crash out
        self.tn.close()
        self.tn = None

class nMediaPCLCD(BaseLCD):
    known_icons = ['BLOCK_FILLED', 'CHECKBOX_GRAY',
                       'HEART_OPEN',      # blank
                       'CHECKBOX_OFF',
                       'CHECKBOX_ON',     # japanese character
                       'SELECTOR_AT_LEFT',
                       'SELECTOR_AT_RIGHT',
                       'ELLIPSIS',        # underscore
                       'FF',              # JP
                       'FR',              # JP
                       'REC'              # small 3 ??!
                       ]
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
    x      = None
    y      = None
    length = None

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

class WidgetFactoryLCD(BaseLCD):
    # widget counter
    ctr = 1

    def incr_ctr(self):
        self.ctr += 1

    def HBargraph(self, x=None, y=None, length=None):
        return HBargraph(self, x, y, length)

    def VBargraph(self, x=None, y=None, length=None):
        return VBargraph(self, x, y, length)

##
## specialized screens
##
class IconFieldLCD(BaseLCD):
    """
    A simple LCD setup such that each cell is filled with an icon
    widget to be manipulated.
    """
    base = 'iconfield'

    def populate_screen(self):
        "Populate our screen with an array of icon widgets."
        self.over_all_cells(lambda x, y: self.widget_add(self.widget_at(x, y), 'icon'))

    def widget_at(self, x, y):
        "Given x and y, what is the widget ID?"
        return self.base + str(x) + str(y)

    def icon_run(self, icon, background='BLOCK_FILLED'):
        if icon == background:
            raise LCDLogicError("senseless to run icon " + icon +
                                " with background " + background)
        prior = None
        def helper(ax, ay):
            nonlocal prior
            this_wid = self.widget_at(ax, ay)
            self.widget_set(this_wid, ax, ay, icon)
            if prior:
                self.widget_set(prior[0], prior[1], prior[2], background)
            prior = [this_wid, ax, ay]
        self.over_all_cells(helper)

    def icon_fill(self, icon):
        self.over_all_cells(lambda x, y: self.widget_set(self.widget_at(x, y), x, y, icon))


class ScrollingTextLCD(BaseLCD):
    """
    Provide the entire LCD as a single wrapped text area, with the 2nd
    line scrolling as needed.
    FIXME: should be flexible for any number of lines
    """
    scrolltextwidgets = []

    def populate_screen(self):
        for i in range(1, self.height):
            self.scrolltextwidgets.append(self.widget_add('line' + str(i), 'string'))
        # final line is different
        self.scrolltextwidgets.append(self.widget_add('line' + str(self.height), 'scroller'))
        self.display('')

    class TextWrapper:
        """
        FIXME: this should be implemented to iterate over
        scrolltextwidgets, really
        """
        def __init__(self, text, lcd):
            (self.text, self.remain, self.lcd) = (text, text, lcd)

        def __iter__(self):
            self.windex = 0     # index into self.lcd.wid
            return self

        def __next__(self):
            if self.remain and self.windex < len(self.lcd.scrolltextwidgets):
                wid = self.lcd.scrolltextwidgets[self.windex]
                line_num = self.windex + 1
                portion = self.remain
                self.windex += 1
                if line_num < self.lcd.height:
                    portion = self.remain[:self.lcd.width]
                    self.remain = self.remain[self.lcd.width:]
                    self.lcd.widget_set(wid, 1, line_num, portion)
                    return portion
                elif line_num == self.lcd.height:  # last line
                    self.lcd.widget_set(wid, 1, line_num, self.lcd.width,
                                        line_num, 'h', 1, self.remain)
                    return self.remain
                else:
                    raise StopIteration
            else:
                raise StopIteration

    def display(self, text):
        for t in ScrollingTextLCD.TextWrapper(text, self):
            if self.debug:
                print("displaying", t)
