#!/opt/rv-Linux-x86-64-7.2.1/bin/py-interp
'''
Module for testing a timeline
'''

import sys
import re

#from PySide import QtGui, QtUiTools, QtCore
from PySide.QtGui import QApplication, QGraphicsRectItem, QColor, QBrush, QPen, QGraphicsScene, QGraphicsLineItem, QGraphicsItemGroup # pylint: disable=E0611,C0301
from PySide.QtUiTools import QUiLoader # pylint: disable=E0611
from PySide.QtCore import Qt # pylint: disable=E0611

frameWidth = 3
trackHeight = 40

def tc2frames(timecode, fps):
    '''
    Converts from timecode to framecount
    '''
    match = re.match(r"(\d{2}):(\d{2}):(\d{2}):(\d{2})", timecode)
    if match is not None:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        frames = int(match.group(4)) + seconds*fps + minutes*60*fps + hours*60*60*fps
        return frames

class clipItem(QGraphicsRectItem):
    '''
    Item for clips in the timeline
    '''
    fill = QBrush(QColor(127, 127, 127), Qt.SolidPattern)
    pen = QPen()
    def __init__(self, startFrame, frames):
        QGraphicsRectItem.__init__(self)
        self.setRect(startFrame*frameWidth, 0, frames*frameWidth, trackHeight)
        self.setBrush(self.fill)
        self.pen.setWidth(2)
        self.setPen(self.pen)

class timelineTrack(QGraphicsItemGroup):
    '''
    Timline track
    '''
    def __init__(self):
        QGraphicsItemGroup.__init__(self)

    def addClip(self, startFrame, frames):
        '''
        Add clip to the track
        '''
        clip = clipItem(startFrame, frames)
        self.scene().addItem(clip)
        self.addToGroup(clip)
        return clip

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

        track = timelineTrack()
        self.addTrack(track)
        self.readEDL(track, 'sample.edl')
        #track.addClip(0, 50)
        #track.addClip(55, 50)

        #marker = timelineMarker()
        #marker.setFrame(40)
        #self.scene.addItem(marker)

        self.mainWindow.show()
        self.app.exec_()

    def readEDL(self, track, edlfile):
        edlFile = open(edlfile)
        for line in edlFile.readlines():
            match = re.match(r"(\d{3})\s+\w+\s+\w+\s+\w+\s+(\d{2}:\d{2}:\d{2}:\d{2}) (\d{2}:\d{2}:\d{2}:\d{2}) (\d{2}:\d{2}:\d{2}:\d{2}) (\d{2}:\d{2}:\d{2}:\d{2})", line)
            if match is not None:
                editStart = tc2frames(match.group(2), 24)
                editEnd = tc2frames(match.group(3), 24)
                editLength = editStart - editEnd
                track.addClip(editStart, editLength)

        edlFile.close()

    def addTrack(self, track):
        '''
        Add track to timeline
        '''
        self.scene.addItem(track)

    """
    def addClip(self, startFrame, frames):
        '''
        Adds a clip to the timeline
        '''
        clip = clipItem(startFrame, frames)

        self.scene.addItem(clip)
        return clip
    """

timelineTest()
