from PyQt4 import QtCore, QtGui, QtNetwork, QtWebKit, QtOpenGL
import InfoMotion
import grabber
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
        self.rotation = 0
        self.rotation_x = 0
        self.rotation_y = 0
        self.translation_x = 0
        self.translation_y = 0
        self.translation_z = 0
        self.zoom = 1

    @staticmethod
    def initPresets():
        effect = AnimationEffect()
        effect.rotation = 90
        effect.translation_x = 100
        AnimationEffect.presets['Rotate and translate'] = effect

        effect = AnimationEffect()
        effect.rotation = 180
        effect.translation_y = 200
        AnimationEffect.presets['Rotate and translate 2'] = effect


class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        #super(MainWindow, self).__init__()
        QtGui.QWidget.__init__(self, parent)
        self.ui = InfoMotion.Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_path = "info_graphic.txt"
        self.grabber = None

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
        self.ui.load_image.clicked.connect(self.loadImageIntoTextAreaPlain)
        self.ui.save_html.clicked.connect(self.generateInfoGraphicString)
        self.ui.save_video.clicked.connect(self.recordVideo)

        # Load info graphic from file
        try:
            self.readFromFile(self.file_path)
        except IOError:
            pass

        # Add first slide and select it if its a new file
        if self.last_slide_count == 1:
            last_item = self.addNewSlide()
        #Otherwise select first slide
        else:
            self.ui.framelist_navigatorView.setCurrentRow(0)

    def recordVideo(self):
        #url = QtCore.QUrl(QtCore.QString("./%1").arg("export.html"))
        url = QtCore.QUrl(QtCore.QString("./%1").arg("demo.html"))
        total_time = 0
        for key, slide in self.slides.items():
            total_time += slide.duration
        total_time = 20 * 1000
        if not self.grabber:
            self.grabber = grabber.GrabberWindow(url, total_time)
        #self.grabber.show()


    def getTextFromContent(self):
        text = self.ui.content_edit.toPlainText()
        return text
        #return self.ui.content_edit.toHtml()

    def closeEvent(self, *args, **kwargs):
        self.saveToFile(self.file_path)

    def saveCurrentSlide(self):
        slide = self.getCurrentSlide()
        slide.html = self.getTextFromContent()
        slide.duration = self.ui.timeout.value()
        slide.effect = self.ui.comboBox.currentText()

    def selectedSlideChanged(self, current, previous):
        # Save previous slide info
        if previous:
            slide = self.slides_by_name[previous.text()]
            slide.html = self.getTextFromContent()
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

    def loadImageIntoTextAreaPlain(self):
        image_path = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open Image"),
                    "", self.tr("Image Files (*.png *.jpg *.bmp)"))
        url = QtCore.QUrl(QtCore.QString("file://%1").arg(image_path))
        cursor = self.ui.content_edit.textCursor()
        img_tag = '\n<img src="{0}" />\n'.format(image_path)
        cursor.insertText(img_tag)

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
        slide.html = self.getTextFromContent()

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

    def createJavascriptTimers(self):
        timers = []
        i = 0
        time_until_now = 0
        for key, value in self.slides.items():
            interval = value.duration * 1000 + time_until_now
            time_until_now += interval
            i += 1
            js = 'var timer' + str(i) + ' = window.setTimeout(function(){  impress().next();}, ' + str(interval) + ' );\n'
            timers.append(js)
        return ''.join(timers)

    def generateInfoGraphicString(self):
        self.saveCurrentSlide()
        with open('template.html', 'r') as f:
            template = f.read()
            content = self.generateToken()
            final_file = template.replace("[content-token]", content)
            final_file = final_file.replace("[transition-duration]", "2000")
            final_file = final_file.replace("[javascript-token]", self.createJavascriptTimers())

        with open('export.html', 'w') as f:
            f.write(final_file)

    def replaceSpaces(self, name):
        return name.replace(" ", "-")
    def generateToken(self):
        slides = []
        x, y, z = 0, 0, 0
        for key, slide in self.slides_by_name.items():
            effect = AnimationEffect.presets[str(slide.effect)]
            x += effect.translation_x
            y += effect.translation_y
            z += effect.translation_z
            one_slide = []
            one_slide.append('<div id="{0}" class="step" data-x="{1}" data-y="{2}" '
                             'data-z="{3}" data-rotate-x="{4}" data-rotate-y="{5}" data-scale="{6}" data-rotate="{7}">'.format(
                self.replaceSpaces(slide.name),
                x, y, z,
                effect.rotation_x, effect.rotation_y, effect.zoom,
                effect.rotation
            ))
            #print slide.html
            one_slide.append(str(slide.html))
            one_slide.append("</div>\n\n")
            slides.append(''.join(one_slide))
        return ''.join(slides)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())