import os
import sys
from PySide2 import QtGui
from PySide2.QtCore import QSizeF, QMarginsF
from PySide2.QtGui import QPainter, QPdfWriter
from PySide2.QtWidgets import QApplication

number = os.environ.get('n', '$n')
expiration = os.environ.get('exp', '$exp')

PT = 1200 / 72
IN = PT * 72
MM = 25.4 / 72

width_pt = 72 * 8.5
height_pt = 72 * 11.0

QApplication([])
writer = QPdfWriter(sys.argv[1])
writer.setPageSizeMM(QSizeF(width_pt * MM, height_pt * MM))
writer.setPageMargins(QMarginsF(0, 0, 0, 0))
painter = QPainter(writer)

y = 9.15 * IN
painter.drawText(3.07 * IN, y, 'X')  # Visa
painter.drawText(6.5 * IN, y, 'X')  # hiker credit on file

y = 9.5 * IN
painter.drawText(0.7 * IN, y, 'Brandon Rhodes')
painter.drawText(6.5 * IN, y, '$226')

y = 10 * IN
painter.drawText(0.7 * IN, y, number)
painter.drawText(6.5 * IN, y, expiration)

y = 10.4 * IN
painter.drawText(6.5 * IN, y, '6/26/2022')

image = QtGui.QImage(os.path.expanduser('~/signature.png'))
pixmap = QtGui.QPixmap(image)
painter.drawPixmap(1.3 * IN, 10.2 * IN, 1.5 * IN, 0.3 * IN, pixmap)

painter.end()
