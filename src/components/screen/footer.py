from .colors import Colors
from .terminal import term


class Footer:

    def __init__(self):

        self.colors = Colors()

    def draw_footer(self, x, y, pages_len=0, active_page=0):

        foot = ""

        with term.location(x, y):

            with term.hidden_cursor():

                for i in range(pages_len):

                    if i == active_page:

                        foot += f"{term.black_on_white}{i}{term.normal} "

                    else:

                        foot += f"{i} "

                print(foot[:-1])
