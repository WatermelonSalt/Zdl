from .screen import term


class Checker:

    def __init__(self):

        self.wrong_dims_msg = f"{term.red_on_black}Please resize your term to a greater size{term.normal}"

    def check(self):

        if (term.width < 80 or term.height < 30) is True:

            with term.hidden_cursor(), term.location(0, term.height//2):

                print(self.wrong_dims_msg.center(
                    term.width + len(term.split_seqs(self.wrong_dims_msg)[0]) + 11, " "))

            return False

        else:

            return True
