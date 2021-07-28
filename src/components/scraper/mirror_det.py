from bs4 import BeautifulSoup
from requests import get


class DetermineMirror:

    def __init__(self):

        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.book_domain = ""

    def determine_mirror(self):

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
