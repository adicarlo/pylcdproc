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


