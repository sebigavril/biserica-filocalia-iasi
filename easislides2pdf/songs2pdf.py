#!/usr/bin/python
# -*- coding: utf-8 -*-

from io import BytesIO
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Spacer

from song import Song

def songs2pdf(songs, pdfFile):
    report = Songs2Pdf()
    report.printSongs(songs, pdfFile)

class Songs2Pdf:
    def __init__(self):
        self.pagesize = A4
        self.width, self.height = self.pagesize

    def printSongs(self, songs, pdfFile):
            pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))
            pdfmetrics.registerFont(TTFont('Calibri Bold', 'Calibrib.ttf'))

            doc = self.docTemaplate(pdfFile)

            styles = getSampleStyleSheet()
            styles.add(self.titleStyle)
            styles.add(self.songTitleStyle)
            styles.add(self.songContentStyle)

            elements = []
            elements.append(Spacer(0, 36))
            elements.append(Paragraph('\t\tCÂNTECE<br />\t\tFILOCALIA', self.titleStyle))
            titlesToFilter = ['Anunț', 'Anunt catiheza', 'Anunt intalnire femei', 'Anunt123', 'Intrbarea zilei', 'Intrebari', 'TACHAT KENAFAV-UNDER HIS WINGS  /TEHILLIM/PSALM 91', 'Telefon', 'Tsama Nafshi (Psalm 42:1-2)']
            filteredSongs = [s for s in songs if len(s.content) != 0 and s.title.encode("utf-8") not in titlesToFilter ]
            for i, song in enumerate(filteredSongs):
                elements.append(PageBreak())
                elements.append(Paragraph(str(i + 1) + '. ' + song.title.upper() + '<br />', self.songTitleStyle))
                elements.append(Spacer(0, 10))
                for j, (key, content) in enumerate(song.content):
                    elements.append(Spacer(0, 10))
                    elements.append(Paragraph(key, self.songContentStyle))
                    elements.append(Paragraph(content.lstrip().rstrip().replace('\n','<br />'), self.songContentStyle))

            doc.build(elements)

    def docTemaplate(self, pdfFile):
        return SimpleDocTemplate(
            pdfFile,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
            pagesize=self.pagesize)

    titleStyle = ParagraphStyle(
        name='filocalia-title',
        alignment=TA_LEFT,
        fontName='Calibri Bold',
        fontSize=36,
        leading=36,
        spaceBefore=200,
        leftIndent=36)

    songTitleStyle = ParagraphStyle(
        name='filocalia-song-title',
        alignment=TA_LEFT,
        fontName='Calibri Bold',
        fontSize=20,
        leading=20 * 1.2)

    songContentStyle = ParagraphStyle(
        name='filocalia-song-content',
        alignment=TA_LEFT,
        fontName='Calibri',
        fontSize=14,
        leading=14 * 1.2)
