from .boxer import enclose_in_box
from .colors import Colors
from .terminal import term


class TextBox:

    def __init__(self):

        self.colors = Colors()

    def draw_active_textbox(self, x: int, y: int, content: str) -> None:

        with term.location(x, y):

            with term.hidden_cursor():

                print(enclose_in_box(
                    content, color=self.colors.textbox_active_color, title_str="Active"))

        return None

    def draw_inactive_textbox(self, x: int, y: int) -> None:

        with term.location(x, y):

            with term.hidden_cursor():

                print(enclose_in_box(
                    "", color=self.colors.textbox_inactive_color, title_str="Inactive"))
