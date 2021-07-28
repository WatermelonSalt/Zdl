from blessed import Terminal

class Checker:

    def __init__(self):

        self.term = Terminal()
        self.wrong_dims_msg = f"{self.term.red_on_black}Please resize your self.term to a greater size{self.term.normal}"

    def check(self):

        if (self.term.width < 80 or self.term.height < 30) is True:

            with self.term.hidden_cursor(), self.term.location(0, self.term.height//2):

                print(self.wrong_dims_msg.center(
                    self.term.width + len(self.term.split_seqs(self.wrong_dims_msg)[0]) + 11, " "))

            return False

        else:

            return True
