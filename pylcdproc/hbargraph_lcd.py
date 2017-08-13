class HBargraphLCD(WidgetFactoryLCD):
    """
    A simple horizontal bargraph, occupying the top row, with text on the 2nd row.
    """

    def populate_screen(self):
        self.graph = self.HBargraph(1, 1, 0)
        self.caption = self.Scroller(1, 2)

    def display(self, value):
        self.graph.update(value)
        self.caption.update(value)
