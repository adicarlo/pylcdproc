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


