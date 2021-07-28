from bs4 import BeautifulSoup
from bs4.element import NavigableString
from requests import get

from .mirror_det import DetermineMirror
from .query_encoder import QueryEncoder


class BookGetter:

    def __init__(self):

        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.determiner = DetermineMirror()
        self.determiner.determine_mirror()
        self.encoder = QueryEncoder(self.determiner.book_domain)

    def make_soup(self, query_string, replace = True):

        query_string = self.encoder.encode_query(query_string, replace)
        book_search_page = get(query_string, headers=self.headers).content
        book_search_soup = BeautifulSoup(book_search_page, "html.parser")

        return book_search_soup

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
                            f"{self.determiner.book_domain}{link_div_element.get('href')}"
                        )

            except TypeError:

                try:

                    for link_div_element in table.find(
                            "div", {"class": "z-book-cover"}):

                        if link_div_element.name == "a":

                            details.append(
                                f"{self.determiner.book_domain}{link_div_element.get('href')}"
                            )

                except TypeError:

                    for link_div_element in table.find(
                            "div", {"class": "z-book-none-cover"}):

                        if link_div_element.name == "a":

                            details.append(
                                f"{self.determiner.book_domain}{link_div_element.get('href')}"
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

    def init_search(self, query_string):

        book_search_soup = self.make_soup(query_string)
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

            for page in range(1, int(reqd_line.split(":")[1].strip()[:-1]) + 1):

                pages.append(f"{query_string}?page={page}")

        except IndexError:

            pass

        return (book_list, pages)
