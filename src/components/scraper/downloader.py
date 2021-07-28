from webbrowser import open as browser_open

class Downloader:

    def __init__(self):

        pass

    def redirect_to_browser(self, body_content, active_element, offset):

        book_link = body_content[active_element + offset][0]
        browser_open(book_link)
