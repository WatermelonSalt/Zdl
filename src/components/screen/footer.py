from blessed import Terminal

from .colors import Colors


class Footer:

    def __init__(self):

        self.term = Terminal()
        self.colors = Colors()

    def draw_footer(self, x, y, pages_len=0, active_page=0):

        foot = ""

        with self.term.location(x, y):

            with self.term.hidden_cursor():

                for i in range(pages_len):

                    if i == active_page:

                        foot += f"{self.term.black_on_white}{i}{self.term.normal} "

                    else:

                        foot += f"{i} "

                print(foot[:-1])
