from typing import Any
from blessed import Terminal

term = Terminal()

def enclose_in_box(title: bool = False, color: str = None, box_chars: tuple = ("║", "═", "╔", "╗", "╚", "╝")):

    def wrap_func(func: Any):

        def wrapper(*args, **kwargs):

            nonlocal title
            nonlocal color
            nonlocal box_chars

            content = args[0]

            if type(content) is str:

                content = [content]

            enclosed = ""

            if color is None:

                color = f"{term.normal}"

            enclosed += f"{color}{box_chars[2]}{box_chars[1]*(term.width - 2)}{box_chars[3]}{term.normal}\n"

            if title:

                for index in range(len(content)):

                    enclosed += f"{color}{box_chars[0]}{term.normal} {content[index].center(term.width - len(term.strip_seqs(content[index])) + (len(content[index]) - 4), ' ')}{term.normal} {color}{box_chars[0]}{term.normal}\n"

            else:

                for index in range(len(content)):

                    enclosed += f"{color}{box_chars[0]}{term.normal} {content[index]}{' '*(term.width - len(term.strip_seqs(content[index])) - 4)}{term.normal} {color}{box_chars[0]}{term.normal}\n"

            enclosed += f"{color}{box_chars[4]}{box_chars[1]*(term.width - 2)}{box_chars[5]}{term.normal}"

            return func(enclosed)

        return wrapper

    return wrap_func
