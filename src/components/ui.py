from blessed import Terminal

from .listener import Listener
from .scraper import BookGetter, Downloader
from .screen import Body, Footer, Header, TextBox


class UI:

    def __init__(self, update_rate):

        self.update_rate = update_rate
        self.textbox_active = False
        self.body_content = []
        self.pages = []
        self.textbox_str = ""
        self.pages_len = len(self.pages)
        self.count = 0
        self.active_index = 0
        self.active_len = 0
        self.offset_index = 0
        self.offsets = 0
        self.active_page = 0
        self.response = ""
        self.header_content = "Z-Library Book Downloader"
        self.listen = Listener()
        self.searcher = BookGetter()
        self.downloader = Downloader()
        self.body = Body(self.update_rate)
        self.footer = Footer()
        self.header = Header()
        self.textbox = TextBox()
        self.term = Terminal()

    def draw_ui(self):

        self.textbox_active, self.active_index, self.active_page, self.active_len, self.offset_index, self.response, self.textbox_str = self.listen.listen(
            1, 4, self.textbox_active, self.active_index, self.active_page, self.active_len, self.offset_index, self.offsets, self.pages_len)

        self.header.draw_head(0, 0, self.header_content)

        if self.textbox_active is False:

            self.textbox.draw_inactive_textbox(0, 3)

        else:

            self.textbox.draw_active_textbox(0, 3, self.textbox_str)

        if self.response == "Get init page":

            self.body_content, self.pages = self.searcher.init_search(
                self.textbox_str)
            self.active_page = 0

        if self.response == "Get active page":

            new_soup = self.searcher.make_soup(self.pages[self.active_page])
            self.body_content = self.searcher.add_books(new_soup)

        if self.response == "Download the current book":

            self.downloader.redirect_to_browser(self.body_content, self.active_index, self.offset_index)

        self.active_len, self.offsets = self.body.draw_body(0, 6, self.body_content, self.offset_index, self.active_index)

        self.footer.draw_footer(0, self.term.height - 2,
                                self.pages_len, self.active_page)

        self.pages_len = len(self.pages)
