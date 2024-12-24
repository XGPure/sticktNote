import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
from Ui_note import *


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton_3.clicked.connect(self.showMinimized)
        self.ui.frame_4.setStyleSheet("font: 15pt;")
        self.default = "border-top: none;border-left: none;border-right: none;border-bottom:1px solid gray;"
        self.changeDefault = "border-top: none;border-left: none;border-right: none;border-bottom:1px solid gray;background-color: rgb(240, 240, 240);"

        self.check_boxes = [
            self.ui.checkBox,
            self.ui.checkBox_2,
            self.ui.checkBox_3,
            self.ui.checkBox_4,
            self.ui.checkBox_5,
            self.ui.checkBox_6,
            self.ui.checkBox_7,
            self.ui.checkBox_8,
        ]

        self.line_edits = [
            self.ui.lineEdit,
            self.ui.lineEdit_2,
            self.ui.lineEdit_3,
            self.ui.lineEdit_4,
            self.ui.lineEdit_5,
            self.ui.lineEdit_6,
            self.ui.lineEdit_7,
            self.ui.lineEdit_8,
        ]

        # 调用函数加载复选框状态和文本框内容
        self.load_all_states()

        # 将checkbox的信号与改变lineEdit的背景连接
        for i in range(len(self.check_boxes)):
            self.check_boxes[i].stateChanged.connect(
                lambda state, index=i: self.change_textedit_style(state, index)
            )

    def change_textedit_style(self, state, index):
        if state == 2:
            # 当对应的CheckBox被选中，设置相应TextEdit的样式表，改变背景颜色
            self.line_edits[index].setStyleSheet(self.changeDefault)
        else:
            # 当CheckBox未被选中，清空相应TextEdit的样式表，恢复默认外观
            self.line_edits[index].setStyleSheet(self.default)

    def load_all_states(self):
        """
        统一加载复选框状态以及文本框中的文本内容
        """
        self.load_checkbox_states()
        self.load_lineedit_texts()

    def load_checkbox_states(self):
        """
        从文件中读取复选框状态信息，并设置对应的复选框状态
        """
        try:
            with open("checkBoxState.txt", "r") as f:
                checkBoxState = f.readlines()
                for i in range(len(self.check_boxes)):
                    self.check_boxes[i].setChecked(
                        self.str_to_bool(checkBoxState[i].strip())
                    )
                    # 新增代码：根据刚加载的复选框状态来更新对应的文本框背景颜色样式
                    state = self.check_boxes[i].isChecked()
                    self.change_textedit_style(2 if state else 0, i)
        except FileNotFoundError:
            print("文件未找到，可能是首次运行")

    def load_lineedit_texts(self):
        """
        从文件中读取文本内容并填充到QLineEdit控件中
        """
        try:
            with open("lineedit_texts.txt", "r") as f:
                lines = f.readlines()
                for i in range(len(self.line_edits)):
                    self.line_edits[i].setText(lines[i].strip())
        except FileNotFoundError:
            print("文件未找到，可能是首次运行")

    def str_to_bool(self, s):
        """
        将字符串转换为布尔值，用于处理从文件中读取的复选框状态字符串
        """
        return s.lower() in ("true", "1")

    def closeEvent(self, event):
        """
        关闭程序时，保存所有QLineEdit控件的文本内容到文件，以及保存复选框状态到文件
        """
        self.save_lineedit_texts()
        self.save_checkbox_states()
        event.accept()

    def save_lineedit_texts(self):
        """
        将所有QLineEdit控件中的文本内容保存到文件
        """
        with open("lineedit_texts.txt", "w") as f:
            for line_edit in self.line_edits:
                text = line_edit.text()
                f.write(text + "\n")

    def save_checkbox_states(self):
        """
        将所有复选框的状态保存到文件
        """
        with open("checkBoxState.txt", "w") as f:
            for checkBox in self.check_boxes:
                text = str(checkBox.isChecked())
                f.write(text + "\n")

    def mousePressEvent(self, event):
        """
        鼠标按下事件处理
        """
        if event.button() == Qt.LeftButton:
            # 记录鼠标按下时相对于屏幕的位置
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """
        鼠标移动事件处理，实现窗口拖拽功能
        """
        if event.buttons() & Qt.LeftButton:
            # 根据鼠标移动的位置来移动窗口
            self.move(event.globalPos() - self.drag_position)
            event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Win = MainWindow()
    Win.show()
    sys.exit(app.exec_())
