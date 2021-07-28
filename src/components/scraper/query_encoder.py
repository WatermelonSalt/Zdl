class QueryEncoder:

    def __init__(self, book_domain):

        self.symbol_dict = {
            r"%": r"%25",
            r" ": r"%20",
            r"!": r"%21",
            r'"': r"%22",
            r'#': r"%23",
            r"$": r"%24",
            r'&': r"%26",
            r"'": r"%27",
            r"(": r"%28",
            r")": r"%29",
            r"*": r"%2A",
            r"+": r"%2B",
            r",": r"%2C",
            r"-": r"%2D",
            r".": r"%2E",
            r"/": r"%2F",
            r":": r"%3A",
            r";": r"%3B",
            r"<": r"%3C",
            r"=": r"%3D",
            r">": r"%3E",
            r"?": r"%3F",
            r"@": r"%40",
            r"[": r"%5B",
            "\\": r"%5C",
            r"]": r"%5D",
            r"^": r"%5E",
            r"_": r"%5F",
            r"`": r"%60",
            r"{": r"%7B",
            r"|": r"%7C",
            r"}": r"%7D",
            r"~": r"%7E"
        }
        self.book_domain = book_domain

    def encode_query(self, query_string, replace):

        if replace:

            for key in self.symbol_dict.keys():

                if key in rf"{query_string}":

                    query_string = query_string.replace(key, self.symbol_dict[key])

        return rf"{self.book_domain}/s/{query_string}"
