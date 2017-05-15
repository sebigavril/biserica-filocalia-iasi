import argparse

from song import Song
from xml2songs import xml2songs
from songs2pdf import songs2pdf

def main():
    parser = argparse.ArgumentParser(description='Convert songs from xml exported from Easislides to PDF')
    parser.add_argument('input', help='path to the exported xml file that serves as input for this script')
    parser.add_argument('output', help='path to the pdf file that will be created')

    input = parser.parse_args().input
    output = parser.parse_args().output

    songs = xml2songs(input)
    songs2pdf(songs, output)


if __name__ == '__main__':
    main()
