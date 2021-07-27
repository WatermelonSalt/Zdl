from typing import Any
from blessed import Terminal

term = Terminal()

def enclose_in_box(content: list, title: bool = False, title_str: str = None, color: str = None, box_chars: tuple = ("║", "═", "╔", "╗", "╚", "╝")):

    if type(content) is str:

        content = [content]

    enclosed = ""

    if color is None:

        color = f"{term.normal}"

    if title_str is None:

        enclosed += f"{color}{box_chars[2]}{box_chars[1]*(term.width - 2)}{box_chars[3]}{term.normal}\n"

    else:

        enclosed += f"{color}{box_chars[2]}{title_str.center(term.width - 2, box_chars[1])}{box_chars[3]}{term.normal}\n"

    if title:

        for index in range(len(content)):

            enclosed += f"{color}{box_chars[0]}{term.normal} {content[index].center(term.width - len(term.strip_seqs(content[index])) + (len(content[index]) - 4), ' ')}{term.normal} {color}{box_chars[0]}{term.normal}\n"

    else:

        for index in range(len(content)):

            enclosed += f"{color}{box_chars[0]}{term.normal} {content[index]}{' '*(term.width - len(term.strip_seqs(content[index])) - 4)}{term.normal} {color}{box_chars[0]}{term.normal}\n"

    enclosed += f"{color}{box_chars[4]}{box_chars[1]*(term.width - 2)}{box_chars[5]}{term.normal}"

    return enclosed
