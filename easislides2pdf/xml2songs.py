import xml.etree.ElementTree

from song import Song

def xml2songs(xmlFile):
    root = xml.etree.ElementTree.parse(xmlFile).getroot()
    items = root.findall('Item')
    return map(__itemToSong, items)

def __itemToSong(item):
    title = item.findtext('Title1')
    rawContent = item.findtext('Contents').encode('utf-8')
    return Song(title, rawContent)
