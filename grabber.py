from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit, QtOpenGL
from PIL import ImageGrab
from cv2 import cv
import time

class GrabberWindow(QtGui.QMainWindow):
    def __init__(self, url):
        QtGui.QMainWindow.__init__(self)

        self.progress = 0
        self.url = url
        QtNetwork.QNetworkProxyFactory.setUseSystemConfiguration(True)
        self.setGeometry(QtCore.QRect(200, 50, 1024, 600))

        # Graphics view
        self.view = QtGui.QGraphicsView()
        self.view.setViewportUpdateMode(QtGui.QGraphicsView.MinimalViewportUpdate)
        self.view.setOptimizationFlags(QtGui.QGraphicsView.DontSavePainterState)
        self.view.setFrameShape(QtGui.QFrame.NoFrame)
        self.view.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.resize(800, 600)

        self.scene_width = 1024
        self.scene_height = 600
        self.view.setSceneRect(QtCore.QRectF(0, 0, self.scene_width, self.scene_height))

        self.view.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)

        # Graphics scene
        self.scene = QtGui.QGraphicsScene()
        self.view.setScene(self.scene)

        # Graphics web view
        self.fast_view = QtWebKit.QGraphicsWebView()
        #self.fast_view.page().setViewportSize(QtCore.QSize(600, 600))
        self.fast_view.resize(1024, 768)
        self.settings = self.fast_view.settings()
        self.settings.setAttribute(QtWebKit.QWebSettings.AcceleratedCompositingEnabled, True)
        #self.settings.setAttribute(QtWebKit.QWebSettings.WebGLEnabled, True)
        #self.settings.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)

        # GL widget for QGraphicsView
        self.qglwidget = QtOpenGL.QGLWidget()
        self.view.setViewport(self.qglwidget)
        self.scene.addItem(self.fast_view)

        # Connect progressions
        #self.fast_view.load(url)

#        viewCaptureAction = QtGui.QAction("Capture", self)
#        viewCaptureAction.triggered.connect(self.initGrab)
#        buttonMenu.addAction(viewCaptureAction)

        self.setCentralWidget(self.view)
        self.openInfographic()


    def openInfographic(self):
        new_url = self.url
        self.fast_view.load(new_url)
        self.fast_view.setFocus()
        self.fast_view.show()

        position_start = self.view.mapToGlobal(self.view.pos())
        position_end = position_start + QtCore.QPoint(self.scene_width, self.scene_height - 100)
        self.geometry = (position_start.x(), position_start.y(), position_end.x(), position_end.y())
        print self.geometry

    def initGrab(self):

        image = ImageGrab.grab(self.geometry)
        cv_im = cv.CreateImageHeader(image.size, cv.IPL_DEPTH_8U, 3)

        cv.SetData(cv_im, image.tostring())

        fourcc = cv.CV_FOURCC('D','I','V','X')
        fps = 25
        width, height = cv.GetSize(cv_im)
        #print width, height
        self.writer = cv.CreateVideoWriter('out3.avi', int(fourcc), fps, (int(width), int(height)), 1)

        cv.WriteFrame(self.writer, cv_im)

        self.frames_count = 1

        timer = QtCore.QTimer()
        time_interval = 1000 / 25
        timer.setInterval(time_interval)
        timer.timeout.connect(self.grabFrame)
        timer.start()
        self.timer = timer

        #secondtimer = QtCore.QTimer()
        #secondtimer.setInterval(100)
        #secondtimer.timeout.connect(self.printNumberOfFrames)
        #secondtimer.start()

        #stopTimer = QtCore.QTimer()
        #stopTimer.setInterval(2000)
        #stopTimer.timeout.connect(self.stopCapture)
        #stopTimer.setSingleShot(True)
        #stopTimer.start()

    def printNumberOfFrames(self):
        print "Number of frames", self.frames_count
        self.frames_count = 0

    def stopCapture(self):
        self.timer.stop()

    def grabFrame(self):

        image = ImageGrab.grab(self.geometry)
        cv_im = cv.CreateImageHeader(image.size, cv.IPL_DEPTH_8U, 3)
        cv.SetData(cv_im, image.tostring())

        cv.WriteFrame(self.writer, cv_im)

        self.frames_count += 1
        print self.frames_count