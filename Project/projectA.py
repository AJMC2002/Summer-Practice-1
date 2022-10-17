import os
import sys
from PIL import Image
from PyQt5 import uic
from PyQt5 import QtWidgets as qtw, QtGui as qtg, QtCore as qtc
from projectB import ConwaysGame


class ASCIIConverter(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.currImg = "-"
        self.CHARS = "$@B%8&WM#ZO0QLCJUYXzcvunxrjft|()1{}[]?-+~<>i!lI;:^'_. "

        uic.loadUi("design/projectA.ui", self)

        self.charSlider.setMaximum(len(self.CHARS))
        self.charSlider.setTickInterval(len(self.CHARS) // 4)
        self.charSlider.setValue(len(self.CHARS) // 2)

        self.addBtn.clicked.connect(lambda: self.addImg())
        self.copyBtn.clicked.connect(lambda: self.copy())
        self.saveBtn.clicked.connect(lambda: self.save())
        self.secretBtn.clicked.connect(lambda: self.secret())
        self.widthSlider.valueChanged.connect(lambda: self.updateScreen())
        self.charSlider.valueChanged.connect(lambda: self.updateScreen())

    def copy(self):
        self.textScreen.selectAll()
        self.textScreen.copy()

    def save(self):
        if self.currImg != "-":
            with open("ascii_img.txt", "w") as fout:
                fout.write(self.textScreen.toPlainText())

    def secret(self):
        if self.currImg != "-":
            img_str, char_subset = self.convert(50, len(self.CHARS) // 2, secret=True)

            matrix = [list(line) for line in img_str.split("\n")]
            for i in range(len(matrix)):
                for j in range(len(matrix[0])):
                    if char_subset.index(matrix[i][j]) > len(char_subset) // 2:
                        matrix[i][j] = 0
                    else:
                        matrix[i][j] = 1

            self.hide()
            ConwaysGame(matrix)
            self.show()

    def resizeAll(self, img_str):
        font = self.textScreen.document().defaultFont()
        text_space = qtg.QFontMetrics(font).size(0, img_str)
        old_w, old_h = self.textScreen.width(), self.textScreen.height()
        new_w, new_h = text_space.width() + 17, text_space.height() + 17

        delta_w = new_w - old_w
        delta_h = new_h - old_h
        w, h = self.width(), self.height()
        w += delta_w
        h += delta_h
        if w < 700:
            w = 700
        if h < 550:
            h = 550
        self.setFixedSize(w, h)
        self.textScreen.setFixedSize(new_w, new_h)

    def convert(self, img_width, char_num, secret=False):
        def resized(img: Image) -> Image:
            width, height = img.size
            ratio = height / width / 1.65
            img_height = int(img_width * ratio)
            resized_img = img.resize((img_width, img_height))
            return resized_img

        def greyify(img: Image) -> Image:
            return img.convert("L")

        def map_pix_to_char(pixels: list, char_subset: list) -> list:
            intensities = sorted(list(set(pixels)))
            pixel_intensities = [intensities.index(pixel) for pixel in pixels]

            intensity_span = len(intensities) - 1
            char_span = len(char_subset) - 1
            mapped_chars = []
            for pixel in pixel_intensities:
                ratio = float(pixel) / float(intensity_span)
                mapped_chars.append(char_subset[-char_span + int(ratio * char_span)])
            return mapped_chars

        def pixels_to_ascii(img: Image) -> str:
            pixels = img.getdata()
            if char_num >= len(self.CHARS):
                char_subset = list(self.CHARS)
            elif char_num % 2 == 0:
                char_subset = (
                    self.CHARS[: (char_num - 1) // 2 + 1]
                    + self.CHARS[len(self.CHARS) - (char_num - 1) // 2 - 1 :]
                )
            else:
                char_subset = (
                    self.CHARS[: (char_num - 1) // 2 + 1]
                    + self.CHARS[len(self.CHARS) - (char_num - 1) // 2 :]
                )
            return "".join(map_pix_to_char(pixels, char_subset)), char_subset

        img = Image.open(self.currImg)
        img_str, char_subset = pixels_to_ascii(greyify(resized(img)))
        pixel_count = len(img_str)
        img_str = "\n".join(
            [img_str[i : (i + img_width)] for i in range(0, pixel_count, img_width)]
        )
        if secret:
            return img_str, char_subset
        else:
            return img_str

    def updateScreen(self):
        if self.currImg != "-":
            img_width = self.widthSlider.value()
            char_num = self.charSlider.value()
            img_str = self.convert(img_width, char_num)
            self.textScreen.clear()
            self.textScreen.setText(img_str)
            self.resizeAll(img_str)

    def addImg(self):
        file_filter = "Images (*.jpg *.jpeg *.png)"
        dialog = qtw.QFileDialog(self)
        response = dialog.getOpenFileName(
            parent=self,
            caption="Выберите изображение",
            directory=os.getcwd(),
            filter=file_filter,
        )
        if response[0]:
            self.currImg = response[0]
            self.currFile.setText(f"Текущее изображение: {self.currImg}")
            self.updateScreen()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = ASCIIConverter()
    window.show()
    sys.exit(app.exec_())
