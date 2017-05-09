import re
import xml.etree.ElementTree

class Song:
    def __init__(self, title, rawContent):
        lyricsNumberOrChrorus = '(\[\d\]|\[chorus\])'

        self.title = title
        self.rawContent = rawContent
        lst = filter(str.strip, re.split(lyricsNumberOrChrorus, rawContent))
        self.content = zip(lst[::2], lst[1::2])

    def __str__(self):
        return str(len(self.content)) + ' : ' + self.title

def itemToSong(item):
    title = item.findtext('Title1').encode('utf-8')
    rawContent = item.findtext('Contents').encode('utf-8')
    return Song(title, rawContent)

def songs(xmlPath):
    root = xml.etree.ElementTree.parse(xmlPath).getroot()
    items = root.findall('Item')
    return map(itemToSong, items)

for song in songs('/Users/s.gavril/Downloads/Export_2017-05-07.xml'):
    print song
