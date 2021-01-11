"""

GPS tracks:

https://www.gaiagps.com/hike/264924/ribbon-falls-via-north-kaibab-trail/
https://www.gaiagps.com/hike/1359/bright-angel-trailhead-via-north-kaibab-trail-and-bright-angel-trail/
https://hikearizona.com/map.php?GPS=10974  [would require free account]

Photos (besides my own):

https://hikearizona.com/decoder.php?ZTN=417

"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

X_RIVER = 263
X_RIBBON_FALLS = 1050
X_COTTONWOOD = 1208
X_MANZANITA = 1352
Y_SEA_LEVEL = 496
Y_6000_FEET = 192
Y_SCALE = (Y_6000_FEET - Y_SEA_LEVEL) / 6000

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1528, 619)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap('section-D.png')
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(10, 10, self.rect().width() -10 , 10)

        # Calibrate
        # w = self.rect().width()
        # painter.drawLine(300, y(0), w - 200, y(6000))

        painter.drawLine(X_RIVER, y(2480), X_RIBBON_FALLS, y(3720))
        painter.drawLine(X_RIBBON_FALLS, y(3720), X_COTTONWOOD, y(4080))
        painter.drawLine(X_COTTONWOOD, y(4080), X_MANZANITA, y(4600))

def y(feet):
    return Y_SEA_LEVEL + Y_SCALE * feet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())
