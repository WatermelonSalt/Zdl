from blessed import Terminal

from .boxer import enclose_in_box
from .colors import Colors


class Header:

    def __init__(self):

        self.term = Terminal()
        self.colors = Colors()

    def draw_head(self, x, y, content):

        with self.term.location(x, y):

            with self.term.hidden_cursor():

                print(enclose_in_box(
                    content, color=self.colors.header_color, title=True))

        return None
