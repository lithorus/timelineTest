#!/opt/rv-Linux-x86-64-7.2.1/bin/py-interp
'''
Module for testing a timeline
'''

import sys

#from PySide import QtGui, QtUiTools, QtCore
from PySide.QtGui import QApplication, QGraphicsRectItem, QColor, QBrush, QGraphicsScene, QGraphicsLineItem # pylint: disable=E0611,C0301
from PySide.QtUiTools import QUiLoader # pylint: disable=E0611
from PySide.QtCore import Qt # pylint: disable=E0611

frameWidth = 3
trackHeight = 40

class clipItem(QGraphicsRectItem):
    '''
    Item for clips in the timeline
    '''
    fill = QBrush(QColor(127, 127, 127), Qt.SolidPattern)
    def __init__(self, startFrame, frames):
        QGraphicsRectItem.__init__(self)
        self.setRect(startFrame*frameWidth, 0, frames*frameWidth, trackHeight)
        self.setBrush(self.fill)

class timelineMarker(QGraphicsLineItem):
    '''
    Line reprensenting the 'cursor'
    '''
    def __init__(self):
        QGraphicsLineItem.__init__(self)
        self.setLine(0, 0, 0, trackHeight)

    def setFrame(self, frame):
        '''
        Move pointer
        '''
        trans = self.transform()
        trans.translate(frame*frameWidth, 0)
        self.setTransform(trans)


class timelineTest(object):
    '''
    Main Class
    '''
    def __init__(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        loader = QUiLoader()
        self.mainWindow = loader.load("timelineTest.ui")
        self.scene = QGraphicsScene()
        self.mainWindow.graphicsView.setScene(self.scene)

        self.addClip(0, 50)
        self.addClip(55, 50)

        marker = timelineMarker()
        marker.setFrame(40)

        '''
        trans = QTransform()
        trans.translate(40, 0)
        marker.setTransform(trans)
        '''

        self.scene.addItem(marker)
        self.mainWindow.show()
        self.app.exec_()

    def addClip(self, startFrame, frames):
        '''
        Adds a clip to the timeline
        '''
        clip = clipItem(startFrame, frames)

        self.scene.addItem(clip)
        return clip

timelineTest()
