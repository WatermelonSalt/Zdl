from .screen import term


class Listener:

    def __init__(self):

        self.count = 0
        self.content = []
        self.tmp_content = []
        self.textbox_str = ""
        self.response = ""

    def listen(self, x, y, textbox_active, active_index, active_page, active_len,  offset_index, offsets, page_len):

        self.response = ""

        with term.cbreak():

            with term.location(x, y):

                inp = term.inkey(timeout=0.0)

                if inp == '\2' and textbox_active is False:

                    textbox_active = True
                    self.count = 0

                if textbox_active is False:

                    self.content = []

                if textbox_active is True:

                    if inp == '\2' and self.count == 1:

                        textbox_active = False

                    self.count = 1
                    self.textbox_str = ""

                    if inp.code == 263:

                        try:

                            self.content.pop()

                        except IndexError:

                            pass

                    if inp.is_sequence is False and inp not in [
                            "", "\x14", "\2"
                    ]:

                        self.content.append(str(inp))

                    self.tmp_content = self.content

                    if len(self.content) > term.width - 4:

                        needed_length = len(self.content) - term.width + 4
                        self.tmp_content = self.tmp_content[needed_length:]

                    for letter in self.tmp_content:

                        self.textbox_str += letter

                    if inp.code == 343:

                        textbox_active = False
                        self.response = "Get init page"

                if textbox_active is False:

                    if inp.lower() == "j":

                        active_index += 1

                    if inp.lower() == "k":

                        active_index -= 1

                    if inp.lower() == "h":

                        active_page -= 1

                    if inp.lower() == "l":

                        active_page += 1

                    if active_index >= active_len:

                        offset_index += 1
                        active_index = active_len - 1

                    if active_index < 0:

                        offset_index -= 1
                        active_index = 0

                    if offset_index < 0:

                        offset_index = offsets
                        active_index = active_len - 1

                    if offset_index > offsets:

                        offset_index = 0
                        active_index = 0

                    if active_page < 0:

                        active_page = page_len - 1

                    if active_page >= page_len:

                        active_page = 0

                    if inp.code == 263:

                        self.response = "Get active page"

                    if inp.code == 343:

                        self.response = "Get init page"

                    if inp.code == 512:

                        self.response = "Download the current book"

        return (textbox_active, active_index, active_page, active_len, offset_index, self.response, self.textbox_str)
