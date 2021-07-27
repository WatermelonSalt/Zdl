from blessed import Terminal, terminal
from boxer import enclose_in_box

term = Terminal()

@enclose_in_box(title=True, color=f"{term.pink}")
def draw_head(content: str) -> None:

    with term.location(0, 0):

        with term.hidden_cursor():

            print(content)

    return None
