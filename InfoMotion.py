# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InfoMotion.ui'
#
# Created: Sat Nov 17 17:14:59 2012
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.content_edit = QtGui.QTextEdit(self.centralwidget)
        self.content_edit.setGeometry(QtCore.QRect(180, 30, 421, 211))
        self.content_edit.setObjectName(_fromUtf8("content_edit"))
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 30, 161, 31))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.load_image = QtGui.QPushButton(self.centralwidget)
        self.load_image.setGeometry(QtCore.QRect(10, 70, 161, 31))
        self.load_image.setObjectName(_fromUtf8("load_image"))
        self.timeout = QtGui.QSpinBox(self.centralwidget)
        self.timeout.setGeometry(QtCore.QRect(130, 110, 41, 31))
        self.timeout.setObjectName(_fromUtf8("timeout"))
        self.duration = QtGui.QLabel(self.centralwidget)
        self.duration.setGeometry(QtCore.QRect(80, 120, 46, 13))
        self.duration.setObjectName(_fromUtf8("duration"))
        self.transition_effects = QtGui.QLabel(self.centralwidget)
        self.transition_effects.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.transition_effects.setObjectName(_fromUtf8("transition_effects"))
        self.frame_content = QtGui.QLabel(self.centralwidget)
        self.frame_content.setGeometry(QtCore.QRect(180, 10, 81, 16))
        self.frame_content.setObjectName(_fromUtf8("frame_content"))
        self.framelist_navigatorView = QtGui.QListView(self.centralwidget)
        self.framelist_navigatorView.setGeometry(QtCore.QRect(610, 30, 181, 511))
        self.framelist_navigatorView.setObjectName(_fromUtf8("framelist_navigatorView"))
        self.frame_navigator = QtGui.QLabel(self.centralwidget)
        self.frame_navigator.setGeometry(QtCore.QRect(610, 10, 91, 16))
        self.frame_navigator.setObjectName(_fromUtf8("frame_navigator"))
        self.frame_nr_ = QtGui.QLabel(self.centralwidget)
        self.frame_nr_.setGeometry(QtCore.QRect(620, 70, 151, 21))
        self.frame_nr_.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.frame_nr_.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_nr_.setObjectName(_fromUtf8("frame_nr_"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(660, 40, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(150, 500, 441, 41))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.preview_button = QtGui.QPushButton(self.splitter)
        self.preview_button.setObjectName(_fromUtf8("preview_button"))
        self.save_html = QtGui.QPushButton(self.splitter)
        self.save_html.setObjectName(_fromUtf8("save_html"))
        self.save_video = QtGui.QPushButton(self.splitter)
        self.save_video.setObjectName(_fromUtf8("save_video"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "InfoMotion", None, QtGui.QApplication.UnicodeUTF8))
        self.load_image.setText(QtGui.QApplication.translate("MainWindow", "Load Image", None, QtGui.QApplication.UnicodeUTF8))
        self.duration.setText(QtGui.QApplication.translate("MainWindow", "Duration", None, QtGui.QApplication.UnicodeUTF8))
        self.transition_effects.setText(QtGui.QApplication.translate("MainWindow", "Transition Effects", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_content.setText(QtGui.QApplication.translate("MainWindow", "Frame Content", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_navigator.setText(QtGui.QApplication.translate("MainWindow", "Frame Navigator", None, QtGui.QApplication.UnicodeUTF8))
        self.frame_nr_.setText(QtGui.QApplication.translate("MainWindow", "Frame N", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Add Frame", None, QtGui.QApplication.UnicodeUTF8))
        self.preview_button.setText(QtGui.QApplication.translate("MainWindow", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.save_html.setText(QtGui.QApplication.translate("MainWindow", "Export to HTML", None, QtGui.QApplication.UnicodeUTF8))
        self.save_video.setText(QtGui.QApplication.translate("MainWindow", "Save VideoMotion", None, QtGui.QApplication.UnicodeUTF8))

