from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QFileDialog
import os
from PyQt5.QtCore import Qt # needs a Qt.KeepAspectRatio constant to resize while maintaining proportions
from PyQt5.QtGui import QPixmap # screen-optimised


from PIL import Image

from PIL import ImageFilter
workdir = ''
class ImageProcessor():
    def __init__(self):
        self.images = None
        self.filename = None
        self.dir = 'dir/'
    def loadimage(self,filename):
        self.filename = filename
        image_path = os.path.join(workdir,filename)
        self.image = Image.open(image_path)
    def showImage(self,path):
        picture.hide()
        pixmapimage = QPixmap(path)
        w,h = picture.width(), picture.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        picture.setPixmap(pixmapimage)
        picture.show()
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir,self.dir,self.filename)
    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir,self.dir,self.filename)
        self.showImage(image_path)
    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir,self.dir,self.filename)
        self.showImage(image_path)
    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir,self.dir,self.filename)
        self.showImage(image_path)
    def sharpness(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir,self.dir,self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(workdir,self.dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)
def choice_workdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
def filter(filenames,extentions):
    result = []
    for filename in filenames:
        for extention in extentions:
            if filename.endswith(extention):
                result.append(filename)
    return result
def showFilenamesList():
    choice_workdir()
    extentions = ['.jpg','.png','.jpeg','.gif','.bmp']
    results = filter(os.listdir(workdir),extentions)
    image_list.clear()
    image_list.addItems(results)
def showChosenImage():
    if image_list.currentRow() >= 0:
        filename = image_list.currentItem().text()
        work_image.loadimage(filename)
        image_path = os.path.join(workdir,work_image.filename)
        work_image.showImage(image_path)


app = QApplication([])
app.setStyleSheet("""
    QWidget {
        background-color: #650032	;
        color: #FFE6F2;
        font-family: 'Consolas';
        font-style: italic ;
    }
    
    QPushButton {
        background-color: #AE0056;
        border: 2px solid #FF80BE;
        border-radius: 4px;
        padding: 8px 12px;
        font-weight: bold;
        min-width: 80px;
        font-size: 17px;
    }
    
    QPushButton:hover {
        background-color: #FF80BE;
        border: 1px solid #7A254F;
        color: #7A254F;
    }

    QPushButton:pressed {
        background-color: #FFE6F2;
        border: 1px solid #7A254F;
        color: #FF80BE;
    }

    QListWidget {
        background-color: #7A254F;
        color: #FF80BE;
        border: 1px solid #FF80BE;
        font-size: 15px;
    }

    QListWidget::Item {
        padding: 5px;
        border-bottom: 1px solid #FF80BE;
    }

    QListWidget::item {
        background-colour: #AE0056;
        color: #FFE6F2;
    }

    QLabel {
     background-color: #7A254F;
        color: #FF80BE;
        border: 3px solid #FF80BE;
        border-radius: 6px;
        qproperty-alignment: AlignCenter;
        font-size: 40px;
        font-weight: bold;
    }

""")
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(700,400)
picture = QLabel('Image')
image_list = QListWidget()
folder_button = QPushButton('Folder')
left_button = QPushButton('Left')
right_button = QPushButton('Right')
mirror_button = QPushButton('Mirror')
sharpness_button = QPushButton('Sharpness')
bw_button = QPushButton('B/W')
main_layout = QHBoxLayout()
bottom_layout = QHBoxLayout()
left_screen_layout = QVBoxLayout()
right_screen_layout = QVBoxLayout()
left_screen_layout.addWidget(folder_button)
left_screen_layout.addWidget(image_list)
bottom_layout.addWidget(left_button)
bottom_layout.addWidget(right_button)
bottom_layout.addWidget(mirror_button)
bottom_layout.addWidget(sharpness_button)
bottom_layout.addWidget(bw_button)
right_screen_layout.addWidget(picture,95)
right_screen_layout.addLayout(bottom_layout)
main_layout.addLayout(left_screen_layout,20)
main_layout.addLayout(right_screen_layout,80)
main_win.setLayout(main_layout)
work_image = ImageProcessor()
folder_button.clicked.connect(showFilenamesList)
bw_button.clicked.connect(work_image.do_bw)
right_button.clicked.connect(work_image.right)
left_button.clicked.connect(work_image.left)
mirror_button.clicked.connect(work_image.mirror)
sharpness_button.clicked.connect(work_image.sharpness)


image_list.currentRowChanged.connect(showChosenImage)
main_win.show()
app.exec()

