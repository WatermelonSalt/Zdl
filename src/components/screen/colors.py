from blessed import Terminal

class Colors:

    term = Terminal()
    header_color = f"{term.pink}"
    textbox_active_color = f"{term.yellow}"
    textbox_inactive_color = f"{term.cyan}"
    body_color = f"{term.color_rgb(118, 255, 33)}"
    footer_color = f"{term.magenta}"
