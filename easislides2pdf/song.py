import re

class Song:
    def __init__(self, title, rawContent):
        lyrics = '(\[[a-zA-Z0-9 ]+\])'

        self.title = title
        self.rawContent = rawContent
        lst = filter(str.strip, re.split(lyrics, rawContent))
        self.content = zip(lst[::2], lst[1::2])

    def __str__(self):
        return str(len(self.content)) + ' : ' + self.title
