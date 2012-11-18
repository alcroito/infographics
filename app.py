from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit, QtOpenGL
import InfoMotion
import sys

class AnimationEffect(object):
    def __init__(self):
        self.rotation_x = 0
        self.rotation_y = 0
        self.translation_x = 0
        self.translation_y = 0
        self.translation_z = 0
        self.zoom = 0
    def initPresets(self):
        self.presets = {}
        effect = AnimationEffect()
        effect.rotation_x = 90
        effect.translation_x = 1000
        self.presets['Rotate and translate'] = effect


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #super(MainWindow, self).__init__()
        QtGui.QWidget.__init__(self, parent)
        self.ui = InfoMotion.Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())