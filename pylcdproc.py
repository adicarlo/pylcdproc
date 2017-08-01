import telnetlib
import re
import time

# custom exceptions
class LCDError(RuntimeError):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

class LCDCommandError(RuntimeError):
    def __init__(self, message, command = 'unknown command'):
        self.message = message
        self.command = command

    def __str__(self):
        return repr(self.message) + ", command: " + repr(self.command)


class LCDLogicError(LCDError): pass
class LCDGarbledSetup(LCDError): pass
class LCDHuhError(LCDCommandError): pass
class LCDProtocolError(LCDCommandError): pass
class LCDNoSuccessError(LCDCommandError): pass


class LCDWidget:
    """
Base class for lcdproc widgets.  Always associated with an LCD.
class BaseLCD:
    """
    lcd    = None
    x      = None
    y      = None
    length = None

    def __init__(self, lcd, x=1, y=1, length=1):
        (self.lcd, self.x, self.y, self.length) = (lcd, x, y, length)
    pass

class HBargraph(LCDWidget):
    pass

class VBargraph(LCDWidget):
    pass

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

    def __init__(self, appname, host='localhost', port=13666, debug=False, priority='foreground'):
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
        self.command_success('widget_add s ' + wid + ' ' + wtype)
        self.widgets.append(wid)

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
        for y in range(1, self.height + 1):
            for x in range(1, self.width + 1):
                func(x, y)

    def dispose(self):
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

class IconFieldLCD(BaseLCD):
    """
    A simple LCD setup such that each cell is filled with an icon widget to be manipulated.
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
            raise LCDLogicError("senseless to run icon " + icon + " with background " + background)
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
    Provide the entire LCD as a single wrapped text area, with the 2nd line scrolling as needed.
    FIXME: should be flexible for any number of lines
    """
    line1wid = "line1"
    line2wid = "line2"

    def populate_screen(self):
        self.widget_add(self.line1wid, 'string')
        self.widget_add(self.line2wid, 'scroller')
        self.display('')

    def display(self, text):
        if len(text) > self.width:
            self.widget_set(self.line1wid, 1, 1, text[:self.width])
            # FIXME: scrolling starts immediately, which is a bit much
            self.widget_set(self.line2wid, 1, self.height, self.width, self.height, 'm', 1, text[self.width:])
        else:
            self.widget_set(self.line1wid, 1, 1, text)

