#!/opt/rv-Linux-x86-64-7.2.1/bin/py-interp
"""
Module for testing a timeline
"""

import sys
import re

from PySide6.QtWidgets import QApplication, QGraphicsRectItem, QGraphicsScene, QGraphicsLineItem, \
    QGraphicsItemGroup, QGraphicsItem
from PySide6.QtGui import QColor, QBrush, QPen
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QPointF

frameWidth = 2
trackHeight = 40

def tc2frames(timecode, fps):
    """
    Converts from timecode to framecount
    """
    match = re.match(r"(\d{2}):(\d{2}):(\d{2}):(\d{2})", timecode)
    if match is not None:
        hours = int(match.group(1))
        minutes = int(match.group(2))
        seconds = int(match.group(3))
        frames = int(match.group(4)) + seconds*fps + minutes*60*fps + hours*60*60*fps
        return frames

class ClipItem(QGraphicsRectItem):
    """
    Item for clips in the timeline
    """
    fill = QBrush(QColor(127, 127, 127), Qt.SolidPattern)
    pen = QPen()
    def __init__(self, startFrame, frames, track):
        self.width = frames * frameWidth
        self.heightNum = 0
        self.height = 1
        super().__init__(0, 0, self.width, trackHeight)
        self.track = track
        self.setPos(startFrame * frameWidth, 0)
        #self.setRect(startFrame*frameWidth, 0, frames*frameWidth, trackHeight)
        self.setBrush(self.fill)
        self.pen.setWidth(2)
        self.setPen(self.pen)
        self.setAcceptHoverEvents(True)
        self.setZValue(0)

    # mouse hover event
    def hoverEnterEvent(self, event):
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        self.setZValue(1)
        orig_position = self.scenePos()
        updated_cursor_x = event.scenePos().x() - event.lastScenePos().x() + orig_position.x()
        self.setPos(QPointF(updated_cursor_x, orig_position.y()))

    def mouseReleaseEvent(self, event):
        self.track.checkBorder(self.scenePos(), self.width)
        self.setZValue(0)
        # print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

class TimelineTrack(object):
    """
    Timline track
    """
    clips = []
    def __init__(self, scene):
        self.scene = scene

    def addClip(self, startFrame, frames):
        """
        Add clip to the track
        """
        clip = ClipItem(startFrame, frames, self)
        self.scene.addItem(clip)
        self.clips.append(clip)
        return clip

    def checkBorder(self, pos, width):
        min_x = pos.x()
        max_x = min_x + width
        for clip in self.clips:
            clip_min_x = clip.scenePos().x()
            clip_max_x = clip_min_x + clip.width
            if clip_min_x < min_x < clip_max_x:
                print(clip)
            elif clip_min_x < max_x < clip_max_x:
                print(clip)


class _TimelineMarker(QGraphicsLineItem):
    """
    Line reprensenting the 'cursor'
    """
    def __init__(self):
        QGraphicsLineItem.__init__(self)
        self.setLine(0, 0, 0, trackHeight)

    def setFrame(self, frame):
        """
        Move pointer
        """
        trans = self.transform()
        trans.translate(frame*frameWidth, 0)
        self.setTransform(trans)


class Timelinetest(object):
    """
    Main Class
    """
    tracks = []
    def __init__(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        loader = QUiLoader()
        self.mainWindow = loader.load("timelineTest.ui")
        self.scene = QGraphicsScene()
        self.mainWindow.graphicsView.setScene(self.scene)

        track = TimelineTrack(self.scene)
        self.addTrack(track)
        self.readEDL(track, 'sample.edl')

        self.mainWindow.show()
        self.app.exec()

    @staticmethod
    def readEDL(track, edlfile):
        """
        Read EDL from file and create clips in track
        """
        edlFile = open(edlfile)
        count = 0
        for line in edlFile.readlines():
            match = re.match(r"(\d{3})\s+\w+\s+\w+\s+\w+\s+(\d{2}:\d{2}:\d{2}:\d{2}) (\d{2}:\d{2}:\d{2}:\d{2}) (\d{2}:\d{2}:\d{2}:\d{2}) (\d{2}:\d{2}:\d{2}:\d{2})", line)
            if match is not None:
                count += 1
                editStart = tc2frames(match.group(4), 24)
                editEnd = tc2frames(match.group(5), 24)
                editLength = editEnd - editStart
                track.addClip(editStart, editLength)

        edlFile.close()

    def addTrack(self, track):
        """
        Add track to timeline
        """
        self.tracks.append(track)


app = QApplication(sys.argv)
Timelinetest()
