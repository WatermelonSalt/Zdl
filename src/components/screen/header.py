from .boxer import enclose_in_box
from .colors import Colors
from .terminal import term


class Header:

    def __init__(self):

        self.colors = Colors()

    def draw_head(self, x, y, content):

        with term.location(x, y):

            with term.hidden_cursor():

                print(enclose_in_box(
                    content, color=self.colors.header_color, title=True))

        return None
