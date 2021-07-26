from time import sleep

from blessed import Terminal
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from requests import get


class process_site_content:
    def __init__(self):

        self.headers = {"User-Agent": "Mozilla/5.0"}

    def determine_book_dl_site_mirror(self):

        mirror_det_page = get("https://z-lib.org",
                              headers=self.headers).content
        mirror_soup = BeautifulSoup(mirror_det_page, "html.parser")

        try:

            for element in mirror_soup.find("div", {"class": "col-sm-4"}):

                if element.name == "a":

                    self.book_domain = "https:" + element.get("href")

        except TypeError:

            exit(
                f"The site returned: {get('https://z-lib.org', headers=self.headers).text}")

    def add_books(self, search_soup):

        book_list = []

        for div in search_soup.find_all("div", {"class": "resItemBox"}):

            details = []
            new_details = []
            authors = []
            book_lang = []
            file_props = []
            rating = []

            table = BeautifulSoup(
                str(
                    BeautifulSoup(str(div), "html.parser").find(
                        "table", {"class": "resItemTable"})), "html.parser")

            try:

                for link_div_element in table.find(
                        "div", {"class": "z-book-precover"}):

                    if link_div_element.name == "a":

                        details.append(
                            f"{self.book_domain}{link_div_element.get('href')}"
                        )

            except TypeError:

                try:

                    for link_div_element in table.find(
                            "div", {"class": "z-book-cover"}):

                        if link_div_element.name == "a":

                            details.append(
                                f"{self.book_domain}{link_div_element.get('href')}"
                            )

                except TypeError:

                    for link_div_element in table.find(
                            "div", {"class": "z-book-none-cover"}):

                        if link_div_element.name == "a":

                            details.append(
                                f"{self.book_domain}{link_div_element.get('href')}"
                            )

            for name_element in table.find("h3", {"itemprop": "name"}):

                if name_element.name == "a":

                    details.append(name_element.contents[0])

            try:

                for publisher_element in table.find("div",
                                                    {"title": "Publisher"}):

                    if publisher_element.name == "a":

                        details.append(publisher_element.contents[0])

            except TypeError:

                details.append([])

            try:

                for author_element in table.find("div", {"class": "authors"}):

                    if author_element.name == "a":

                        authors.append(author_element.contents[0])

            except (TypeError, IndexError):

                authors.append([])

            details.append(authors)

            try:

                for language_prop in table.find(
                        "div", {"class": "property_language"}):

                    if type(language_prop) is not NavigableString:

                        if language_prop.get("class") in [["property_label"],
                                                          ["property_value"]]:

                            book_lang.append(language_prop.contents[0].strip())

            except TypeError:

                book_lang.append([])

            details.append(book_lang)

            try:

                for file_prop in table.find("div",
                                            {"class": "property__file"}):

                    if type(file_prop) is not NavigableString:

                        if file_prop.get("class") in [["property_label"],
                                                      ["property_value"]]:

                            file_props.append(file_prop.contents[0].strip())

            except:

                file_props.append([])

            details.append(file_props)

            for rating_prop in table.find("div", {"class": "book-rating"}):

                if type(rating_prop) is not NavigableString:

                    if "book-rating-interest-score" in rating_prop.get(
                            "class"):

                        rating.append("Rating:")
                        rating.append(rating_prop.contents[0].strip())

            details.append(rating)

            new_details = details

            for index, detail in enumerate(details):

                if type(detail) == list:

                    if len(detail) == 0:

                        pass

                    else:

                        append_str = f"{detail[0]} "

                        for thingy in range(1, len(detail)):

                            append_str += f"{detail[thingy]}"

                        new_details[index] = append_str

            book_list.append(new_details)

        return book_list

    def encode_query_string(self, query_string: str):

        query_string = query_string.replace("#", "%23")
        query_string = query_string.replace("&", "%26")
        query_string = query_string.replace(" ", "%20")
        query_string = f"{self.book_domain}/s/" + query_string

        return query_string

    def get_book_search_results(self, query_string: str):

        query_string = self.encode_query_string(query_string)
        book_search_page = get(query_string, headers=self.headers).content
        book_search_soup = BeautifulSoup(book_search_page, "html.parser")
        pages = []
        reqd_script = ""
        reqd_line = ""

        book_list = self.add_books(book_search_soup)

        for script in book_search_soup.find_all("script"):

            for line in script.contents:

                if "pagesTotal" in line.strip():

                    reqd_script = line.strip()

        for line in reqd_script.split("\n"):

            if "pagesTotal" in line:

                reqd_line = line.strip()

        try:

            for page in range(2, int(reqd_line.split(":")[1].strip()[:-1]) + 1):

                pages.append(f"{query_string}?page={page}")

        except IndexError:

            pass

        return (book_list, pages)

    def get_book(self):

        pass


class draw_screen:
    def __init__(self):

        self.term = Terminal()
        self.active_offset = 0
        self.active_prev = 0
        self.call_count = 0
        self.offset_str_call_count = 0
        self.str1_offset = 0
        self.comp_str1 = ""

    def enclose_in_box(self,
                       content: list,
                       title: bool = False,
                       box_color: str = None) -> str:

        if box_color is None:

            box_color = f"{self.term.normal}"

        enclosed = ""
        box_chars = ["║", "═", "╔", "╗", "╚", "╝"]

        enclosed += f"{box_color}{box_chars[2]}{box_chars[1]*(self.term.width - 2)}{box_chars[3]}{self.term.normal}\n"

        if title:

            for index in range(len(content)):

                enclosed += f"{box_color}{box_chars[0]}{self.term.normal} {content[index].center(self.term.width - len(self.term.strip_seqs(content[index])) + (len(content[index]) - 4), ' ')}{self.term.normal} {box_color}{box_chars[0]}{self.term.normal}\n"

        else:

            for index in range(len(content)):

                enclosed += f"{box_color}{box_chars[0]}{self.term.normal} {content[index]}{' '*(self.term.width - len(self.term.strip_seqs(content[index])) - 4)}{self.term.normal} {box_color}{box_chars[0]}{self.term.normal}\n"

        enclosed += f"{box_color}{box_chars[4]}{box_chars[1]*(self.term.width - 2)}{box_chars[5]}{self.term.normal}"

        return enclosed

    def draw_title(self, content: str, box_color: str = None):

        with self.term.location(0, 0), self.term.hidden_cursor():

            print(
                self.enclose_in_box([content], title=True,
                                    box_color=box_color))

    def draw_textbox(self, content: str, box_color: str = None):

        with self.term.location(0, 3), self.term.hidden_cursor():

            print(self.enclose_in_box([content], box_color=box_color))

    def draw_body(self, content: list, update_rate: int, box_color: str = None, offset: int = 0, active: int = 0):

        content_disp = []
        self.call_count += 1
        self.offset_str_call_count += 1

        if self.call_count >= 3*((1/update_rate)/4):

            self.call_count = 0
            self.active_offset += 1

        if self.offset_str_call_count >= (1/update_rate)/4:

            self.offset_str_call_count = 0
            self.str1_offset += 1

        if self.str1_offset >= len(self.comp_str1) - 49:

            self.str1_offset = 0

        if self.active_offset == 5:

            self.active_offset = 0

        if self.active_prev != active:

            self.active_offset = 0

        with self.term.location(0, 6), self.term.hidden_cursor():

            if len(content) < self.term.height - 10:

                for i in range(self.term.height - 10):

                    if len(content) == self.term.height - 10:

                        break

                    content.append("")

            if len(content) > self.term.height - 10:

                content = content[offset: self.term.height + offset - 10]

            for info in content:

                if type(info) == list:

                    content_disp.append(info[1])

                else:

                    content_disp.append(info)

            if type(content[active]) == list:

                content_disp[active] = f"{self.term.black_on_grey}{content[active][1].strip()}  {content[active][2 + self.active_offset].strip()}{self.term.normal}"

            else:

                content_disp[active] = f"{self.term.black_on_grey}{content[active].strip()}{self.term.normal}"

            for index, elem in enumerate(content_disp):

                if len(elem) > self.term.width - 4:

                    if index == active:

                        self.comp_str1 = content[active][1].strip()

                        content_disp[active] = f"{self.term.black_on_grey}" + f"{content[active][1].strip()[self.str1_offset: self.str1_offset + 50]}  {content[active][2 + self.active_offset].strip()}"[
                            : self.term.width - 4] + f"{self.term.normal}"

                    else:

                        content_disp[index] = content_disp[index][:self.term.width - 4]

            self.active_prev = active

            print(self.enclose_in_box(content_disp, box_color=box_color))


if __name__ == "__main__":

    screen = draw_screen()
    terminal = Terminal()
    book_processor = process_site_content()
    book_processor.determine_book_dl_site_mirror()
    update_rate = 1/4

    try:

        with terminal.hidden_cursor(), terminal.fullscreen():

            textbox_active = False
            content = []
            tmp_content = []
            body_content = []
            pages = 0
            count = 0
            wrong_dimensions_message = f"{terminal.red_on_black}Please resize your terminal to a greater size{terminal.normal}"

            while True:

                if (terminal.width < 80 or terminal.height < 30) is True:

                    with terminal.hidden_cursor(), terminal.location(0, terminal.height//2):

                        print(wrong_dimensions_message.center(terminal.width + len(terminal.split_seqs(wrong_dimensions_message)[0]) + 11, " "))

                else:

                    with terminal.cbreak(), terminal.location(1, 4):

                        input = terminal.inkey(timeout=0.0)

                        if input == '\2' and textbox_active is False:

                            textbox_active = True
                            count = 0

                        if textbox_active is False:

                            content = []

                        if textbox_active is True:

                            if input == '\2' and count == 1:

                                textbox_active = False

                            count = 1
                            final_str = ""

                            if input.code == 263:

                                try:

                                    content.pop()

                                except IndexError:

                                    pass

                            if input.is_sequence is False and input not in [
                                    "", "\x14", "\2"
                            ]:

                                content.append(str(input))

                            tmp_content = content

                            if len(content) > terminal.width - 4:

                                needed_length = len(content) - terminal.width + 4
                                tmp_content = tmp_content[needed_length:]

                            for letter in tmp_content:

                                final_str += letter

                            if input.code == 343 and textbox_active is True:

                                textbox_active = False
                                body_content, pages = book_processor.get_book_search_results(
                                    final_str)

                    screen.draw_title(
                        f"{terminal.pink}Z-Library Books Downloader{terminal.normal}",
                        box_color=f"{terminal.lightgreen}")

                    if textbox_active is False:

                        screen.draw_textbox("")

                    if textbox_active is True:

                        screen.draw_textbox(final_str,
                                            box_color=f"{terminal.magenta}")

                    screen.draw_body(
                        body_content, update_rate=update_rate, box_color=f"{terminal.yellow}")

                sleep(update_rate)

    except KeyboardInterrupt:

        exit()
