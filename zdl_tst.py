from src.components import UI
from src.components import Checker
from blessed import Terminal
from time import sleep

if __name__ == "__main__":

    term = Terminal()
    update_rate = 1/24
    interface = UI(update_rate)
    checker = Checker()

    try:

        with term.fullscreen():

            while True:

                if checker.check():

                    interface.draw_ui()
                    sleep(update_rate)

    except KeyboardInterrupt:

        exit()
