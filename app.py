from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit, QtOpenGL
import InfoMotion
import sys
import pickle

class Slide(object):
    def __init__(self):
        self.html = QtCore.QString()
        self.effect = QtCore.QString()
        self.name = QtCore.QString()
        self.duration = 1
        pass

class AnimationEffect(object):
    presets = {}
    def __init__(self):
        self.rotation_x = 0
        self.rotation_y = 0
        self.translation_x = 0
        self.translation_y = 0
        self.translation_z = 0
        self.zoom = 0

    @staticmethod
    def initPresets():
        effect = AnimationEffect()
        effect.rotation_x = 90
        effect.translation_x = 1000
        AnimationEffect.presets['Rotate and translate'] = effect

        effect = AnimationEffect()
        effect.rotation_y = 180
        effect.translation_y = 500
        AnimationEffect.presets['Rotate and translate 2'] = effect


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #super(MainWindow, self).__init__()
        QtGui.QWidget.__init__(self, parent)
        self.ui = InfoMotion.Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_path = "info_graphic.txt"

        self.slides = {}
        self.slides_by_name = {}
        self.last_slide_count = 1

        # Populate initial effect presets
        AnimationEffect.initPresets()
        self.ui.comboBox.setInsertPolicy(QtGui.QComboBox.InsertAtBottom)
        sorted_keys = AnimationEffect.presets.keys()
        sorted_keys.sort()
        for key in sorted_keys:
            self.ui.comboBox.addItem(key)

        # Connect events
        self.ui.addFrameButton.clicked.connect(self.addNewSlide)
        self.ui.framelist_navigatorView.currentItemChanged.connect(self.selectedSlideChanged)
        self.ui.load_image.clicked.connect(self.loadImageIntoTextArea)

        # Load info graphic from file
        self.readFromFile(self.file_path)

        # Add first slide and select it if its a new file
        if self.last_slide_count == 1:
            last_item = self.addNewSlide()
        #Otherwise select first slide
        else:
            self.ui.framelist_navigatorView.setCurrentRow(0)


    def closeEvent(self, *args, **kwargs):
        self.saveToFile(self.file_path)

    def selectedSlideChanged(self, current, previous):
        # Save previous slide info
        if previous:
            slide = self.slides_by_name[previous.text()]
            slide.html = self.ui.content_edit.toHtml()
            slide.duration = self.ui.timeout.value()
            slide.effect = self.ui.comboBox.currentText()

        # Load new slide info
        slide = self.slides_by_name[current.text()]
        self.ui.content_edit.setHtml(slide.html)
        self.ui.timeout.setValue(slide.duration)
        comboIndex = self.ui.comboBox.findText(slide.effect)
        if comboIndex != -1:
            self.ui.comboBox.setCurrentIndex(comboIndex)
        else:
            self.ui.comboBox.setCurrentIndex(0)

    def addNewSlide(self):
        name = self.tr("Slide %n", "", self.last_slide_count)
        item = QtGui.QListWidgetItem(name, self.ui.framelist_navigatorView)
        slide = Slide()
        slide.name = name
        self.slides_by_name[name] = slide
        self.slides[self.last_slide_count] = slide
        self.last_slide_count += 1

        self.ui.framelist_navigatorView.setCurrentItem(item)
        return item

    def getCurrentSlide(self):
        item = self.ui.framelist_navigatorView.currentItem()
        return self.slides_by_name[item.text()]

    def loadImageIntoTextArea(self):
        image_path = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open Image"),
            "", self.tr("Image Files (*.png *.jpg *.bmp)"))
        url = QtCore.QUrl(QtCore.QString("file://%1").arg(image_path))

        image = QtGui.QImageReader(image_path).read()
        document = QtGui.QTextDocument = self.ui.content_edit.document()
        document.addResource(QtGui.QTextDocument.ImageResource, url, QtCore.QVariant(image))

        cursor = self.ui.content_edit.textCursor()
        imageFormat = QtGui.QTextImageFormat()
        imageFormat.setWidth(50)
        imageFormat.setHeight(50)
        imageFormat.setName(url.toString())
        cursor.insertImage(imageFormat)

        slide = self.getCurrentSlide()
        slide.html = self.ui.content_edit.toHtml()

    def saveToFile(self, path):
        with open(path, 'w') as f:
            pickle.dump(self.slides, f)
            pickle.dump(self.slides_by_name, f)
            pickle.dump(self.last_slide_count, f)

    def updateWidgetsAfterLoad(self):
        self.ui.framelist_navigatorView.clear()
        for name, slide in self.slides_by_name.items():
            QtGui.QListWidgetItem(name, self.ui.framelist_navigatorView)
            pass
        self.ui.content_edit.setFocus()

    def readFromFile(self, path):
        with open(path, 'r') as f:
            self.slides = pickle.load(f)
            self.slides_by_name = pickle.load(f)
            self.last_slide_count = pickle.load(f)
            self.updateWidgetsAfterLoad()

    def generateInfoGraphicString(self):
        pass

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())