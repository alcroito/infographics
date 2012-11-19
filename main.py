#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
###########################################################################


from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit, QtOpenGL
from PIL import ImageGrab
from cv2 import cv

import time

class MainWindow(QtGui.QMainWindow):
    def __init__(self, url):
        super(MainWindow, self).__init__()

        self.progress = 0

        fd = QtCore.QFile(":/jquery.min.js")

        if fd.open(QtCore.QIODevice.ReadOnly | QtCore.QFile.Text):
            self.jQuery = QtCore.QTextStream(fd).readAll()
            fd.close()
        else:
            self.jQuery = ''

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
        #self.view.set

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
        self.settings.setAttribute(QtWebKit.QWebSettings.WebGLEnabled, True)
        self.settings.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)

        # GL widget for QGraphicsView
        self.qglwidget = QtOpenGL.QGLWidget()
        self.view.setViewport(self.qglwidget)
        self.scene.addItem(self.fast_view)

        # Connect progressions
        self.fast_view.load(url)
        self.fast_view.loadFinished.connect(self.adjustLocation)
        self.fast_view.titleChanged.connect(self.adjustTitle)
        self.fast_view.loadProgress.connect(self.setProgress)
        self.fast_view.loadFinished.connect(self.finishLoading)

        # Location
        self.locationEdit = QtGui.QLineEdit(self)
        self.locationEdit.setSizePolicy(QtGui.QSizePolicy.Expanding,
                self.locationEdit.sizePolicy().verticalPolicy())
        self.locationEdit.returnPressed.connect(self.changeLocation)

        # Toolbar
        toolBar = self.addToolBar("Navigation")
        toolBar.addAction(self.fast_view.pageAction(QtWebKit.QWebPage.Back))
        toolBar.addAction(self.fast_view.pageAction(QtWebKit.QWebPage.Forward))
        toolBar.addAction(self.fast_view.pageAction(QtWebKit.QWebPage.Reload))
        toolBar.addAction(self.fast_view.pageAction(QtWebKit.QWebPage.Stop))
        toolBar.addWidget(self.locationEdit)


        # Menu bar
        viewMenu = self.menuBar().addMenu("&View")
        viewSourceAction = QtGui.QAction("Page Source", self)
        viewSourceAction.triggered.connect(self.viewSource)
        viewMenu.addAction(viewSourceAction)

        # Button
        buttonMenu = self.menuBar().addMenu("&Open Infographic")
        openAction = QtGui.QAction("Open", self)
        openAction.triggered.connect(self.openInfographic)
        buttonMenu.addAction(openAction)

        viewCaptureAction = QtGui.QAction("Capture", self)
        viewCaptureAction.triggered.connect(self.initGrab)
        buttonMenu.addAction(viewCaptureAction)

        #
        effectMenu = self.menuBar().addMenu("&Effect")
        effectMenu.addAction("Highlight all links", self.highlightAllLinks)

        self.rotateAction = QtGui.QAction(
                self.style().standardIcon(
                        QtGui.QStyle.SP_FileDialogDetailedView),
                "Turn images upside down", self, checkable=True,
                toggled=self.rotateImages)
        effectMenu.addAction(self.rotateAction)

        toolsMenu = self.menuBar().addMenu("&Tools")
        toolsMenu.addAction("Remove GIF images", self.removeGifImages)
        toolsMenu.addAction("Remove all inline frames",
                self.removeInlineFrames)
        toolsMenu.addAction("Remove all object elements",
                self.removeObjectElements)
        toolsMenu.addAction("Remove all embedded elements",
                self.removeEmbeddedElements)


        self.setCentralWidget(self.view)
        self.setUnifiedTitleAndToolBarOnMac(True)

    def viewSource(self):
        accessManager = self.fast_view.page().networkAccessManager()
        request = QtNetwork.QNetworkRequest(self.fast_view.url())
        reply = accessManager.get(request)
        reply.finished.connect(self.slotSourceDownloaded)

    def slotSourceDownloaded(self):
        reply = self.sender()
        self.textEdit = QtGui.QTextEdit(None)
        self.textEdit.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.textEdit.show()
        self.textEdit.setPlainText(QtCore.QTextStream(reply).readAll())
        self.textEdit.resize(600, 400)
        reply.deleteLater()

    def adjustLocation(self):
        self.locationEdit.setText(self.fast_view.url().toString())

    def openInfographic(self):
        #new_url = QtCore.QUrl.fromLocalFile("D:/Web/infographics/bartaz/test2.html")
        new_url = QtCore.QUrl.fromLocalFile("D:/Web/infographics/demo.html")
        self.fast_view.load(new_url)
        self.fast_view.setFocus()

        position_start = self.view.mapToGlobal(self.view.pos())
        position_end = position_start + QtCore.QPoint(self.scene_width, self.scene_height - 100)
        self.geometry = (position_start.x(), position_start.y(), position_end.x(), position_end.y())
        print self.geometry

        #self.grabFrame()

    def changeLocation(self):
        url = QtCore.QUrl.fromUserInput(self.locationEdit.text())
        self.fast_view.load(url)
        self.fast_view.setFocus()

    def adjustTitle(self):
        if 0 < self.progress < 100:
            self.setWindowTitle("%s (%s%%)" % (self.fast_view.title(), self.progress))
        else:
            self.setWindowTitle(self.fast_view.title())

    def setProgress(self, p):
        self.progress = p
        self.adjustTitle()

    def finishLoading(self):
        self.progress = 100
        self.adjustTitle()
        #self.fast_view.page().mainFrame().evaluateJavaScript(self.jQuery)
        #self.rotateImages(self.rotateAction.isChecked())

    def highlightAllLinks(self):
        code = """$('a').each(
                    function () {
                        $(this).css('background-color', 'yellow') 
                    } 
                  )"""
        self.fast_view.page().mainFrame().evaluateJavaScript(code)

    def rotateImages(self, invert):
        if invert:
            code = """
                $('img').each(
                    function () {
                        $(this).css('-webkit-transition', '-webkit-transform 2s'); 
                        $(this).css('-webkit-transform', 'rotate(180deg)') 
                    } 
                )"""
        else:
            code = """
                $('img').each(
                    function () { 
                        $(this).css('-webkit-transition', '-webkit-transform 2s'); 
                        $(this).css('-webkit-transform', 'rotate(0deg)') 
                    } 
                )"""

        self.fast_view.page().mainFrame().evaluateJavaScript(code)

    def removeGifImages(self):
        code = "$('[src*=gif]').remove()"
        self.fast_view.page().mainFrame().evaluateJavaScript(code)

    def removeInlineFrames(self):
        code = "$('iframe').remove()"
        self.fast_view.page().mainFrame().evaluateJavaScript(code)

    def removeObjectElements(self):
        code = "$('object').remove()"
        self.fast_view.page().mainFrame().evaluateJavaScript(code)

    def removeEmbeddedElements(self):
        code = "$('embed').remove()"
        self.fast_view.page().mainFrame().evaluateJavaScript(code)

    def initGrab(self):
        start = time.clock()
        elapsed = time.clock()
        elapsed -= start
        #print "Time spent in (Qt image grab) is: %0.3f ms\n" % (elapsed * 1000)

        image_qt = QtGui.QPixmap.grabWidget(self.view)
        image_qt_i = image_qt.toImage()
        i2 = image_qt_i.convertToFormat(QtGui.QImage.Format_RGB888)
        i3 = i2.rgbSwapped()
        i3_bits = i3.bits()
        image_qt_size = (i3.size().width(), i3.size().height())
        #image = ImageGrab.grab(self.geometry)
        cv_im = cv.CreateImageHeader(image_qt_size, cv.IPL_DEPTH_8U, 3)

        cv.SetData(cv_im, i3_bits.asstring(i3.numBytes()))

        fourcc = cv.CV_FOURCC('D','I','V','X')
        fps = 25
        width, height = cv.GetSize(cv_im)
        #print width, height
        self.writer = cv.CreateVideoWriter('out3.avi', int(fourcc), fps, (int(width), int(height)), 1)

        start = time.time()
        cv.WriteFrame(self.writer, cv_im)
        elapsed = time.time()
        elapsed -= start
        #print "Time spent in (Write Frame) is:%0.3f ms \n" % (elapsed * 1000)

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

        start = time.clock()
        image_qt = QtGui.QPixmap.grabWidget(self.view).toImage()
        #i2 = image_qt_i.convertToFormat(QtGui.QImage.Format_RGB888)
        #i3 = i2.rgbSwapped()
        #i3_bits = i3.bits()
        #image_qt_size = (i3.size().width(), i3.size().height())
        #image = ImageGrab.grab(self.geometry)
        image_qt_size = (image_qt.size().width(), image_qt.size().height())
        cv_im_4chan = cv.CreateImageHeader(image_qt_size, cv.IPL_DEPTH_8U, 4)
        cv_im = cv.CreateImage(image_qt_size, cv.IPL_DEPTH_8U, 3)

        cv.SetData(cv_im_4chan, image_qt.bits().asstring(image_qt.numBytes()))
        cv.CvtColor(cv_im_4chan, cv_im, cv.CV_RGBA2RGB)
        elapsed = time.clock()
        elapsed -= start
        #print "Time spent in (Qt image grab) is: %0.3f ms" % elapsed

        start = time.time()
        cv.WriteFrame(self.writer, cv_im)
        elapsed = time.time()
        elapsed = elapsed - start
       # print "Time spent in (Write Frame) is:%0.3f ms " % elapsed * 1000

        self.frames_count += 1
        #print self.frames_count

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    #if len(sys.argv) > 1:
    #    url = QtCore.QUrl(sys.argv[1])
    #else:
    #    url = QtCore.QUrl('http://www.google.com/ncr')

    #url = QtCore.QUrl.fromLocalFile("D:/Web/infographics/bartaz/test2.html")

    url = QtCore.QUrl()
    browser = MainWindow(url)
    browser.show()

    sys.exit(app.exec_())
