from .boxer import enclose_in_box
from .colors import Colors
from .terminal import term


class Body:

    def __init__(self, update_rate):

        self.colors = Colors()
        self.active_offset = 0
        self.active_prev = 0
        self.call_count = 0
        self.offset_str_call_count = 0
        self.str1_offset = 0
        self.comp_str1 = ""
        self.update_rate = update_rate

    def draw_body(self, x: int, y: int, content: str, offset: int = 0, active: int = 0) -> tuple:

        content_disp = []
        self.call_count += 1
        self.offset_str_call_count += 1

        if self.call_count >= 3*((1/self.update_rate)/4):

            self.call_count = 0
            self.active_offset += 1

        if self.offset_str_call_count >= (1/self.update_rate)/4:

            self.offset_str_call_count = 0
            self.str1_offset += 1

        if self.str1_offset >= len(self.comp_str1) - 49:

            self.str1_offset = 0

        if self.active_offset == 5:

            self.active_offset = 0

        if self.active_prev != active:

            self.active_offset = 0

        orig_content_length = len(content)

        if len(content) < term.height - 10:

            for i in range(term.height - 10):

                if len(content) == term.height - 10:

                    break

                content.append("")

        if len(content) > term.height - 10:

            content = content[offset: term.height + offset - 10]

        for info in content:

            if type(info) == list:

                content_disp.append(info[1])

            else:

                content_disp.append(info)

        if type(content[active]) == list:

            content_disp[active] = f"{term.black_on_grey}{content[active][1]}  {content[active][2 + self.active_offset]}{term.normal}"

        else:

            content_disp[active] = f"{term.black_on_grey}{content[active]}{term.normal}"

        for index, elem in enumerate(content_disp):

            if len(elem) > term.width - 4:

                if index == active:

                    self.comp_str1 = content[active][1]

                    content_disp[active] = f"{term.black_on_grey}" + f"{content[active][1][self.str1_offset: self.str1_offset + 50]}  {content[active][2 + self.active_offset]}"[
                        : term.width - 4] + f"{term.normal}"

                else:

                    content_disp[index] = content_disp[index][:term.width - 4]

        self.active_prev = active

        with term.location(x, y):

            with term.hidden_cursor():

                print(enclose_in_box(content_disp, color=self.colors.body_color))

        return (len(content_disp), orig_content_length - len(content_disp))
