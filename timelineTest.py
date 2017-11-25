#!/opt/rv-Linux-x86-64-7.2.1/bin/py-interp
'''
Module for testing a timeline
'''

import sys

#from PySide import QtGui, QtUiTools, QtCore
from PySide.QtGui import QApplication, QGraphicsRectItem, QColor, QBrush, QGraphicsScene # pylint: disable=E0611
from PySide.QtUiTools import QUiLoader # pylint: disable=E0611
from PySide.QtCore import Qt # pylint: disable=E0611

class clipItem(QGraphicsRectItem):
    '''
    Item for clips in the timeline
    '''
    height = 40
    frameWidth = 3
    fill = QBrush(QColor(127, 127, 127), Qt.SolidPattern)
    def __init__(self, startFrame, frames):
        QGraphicsRectItem.__init__(self)
        self.setRect(startFrame*self.frameWidth, 0, frames*self.frameWidth, self.height)
        self.setBrush(self.fill)


class timelineTest(object):
    '''
    Main Class
    '''
    #mainWindow = QtGui.QMainWindow()
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
