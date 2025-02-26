# coding:utf-8
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QToolButton


class BasicButton(QToolButton):
    """ 基本六态按钮 """

    def __init__(self, iconPathDict_list: list, parent=None, iconSize_tuple: tuple = (57, 40)):
        super().__init__(parent=parent)
        self.iconPathDict_list = iconPathDict_list
        self.iconWidth, self.iconHeight = iconSize_tuple
        # 图标颜色标志位
        self.isWhiteIcon = False
        # 初始化
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.resize(self.iconWidth, self.iconHeight)
        self.setIconSize(QSize(self.width(), self.height()))
        self.setStyleSheet("border: none; margin: 0px")
        self.__updateIcon("normal")

    def enterEvent(self, e):
        """ hover时更换图标 """
        self.__updateIcon("hover")

    def leaveEvent(self, e):
        """ leave时更换图标 """
        self.__updateIcon("normal")

    def mousePressEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.__updateIcon("pressed")
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """ 鼠标松开时更换按钮图标 """
        if e.button() == Qt.RightButton:
            return
        self.__updateIcon("normal")
        super().mouseReleaseEvent(e)

    def setWhiteIcon(self, isWhite: bool):
        """ 设置图标颜色 """
        self.isWhiteIcon = isWhite
        self.__updateIcon("normal")

    def __updateIcon(self, iconState: str):
        """ 更新图标 """
        self.setIcon(
            QIcon(self.iconPathDict_list[self.isWhiteIcon][iconState]))


class MaximizeButton(QPushButton):
    """ 定义最大化按钮 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iconPathDict_list = [
            [
                {
                    "normal": ":/images/title_bar/透明黑色最大化按钮_57_40.png",
                    "hover": ":/images/title_bar/绿色最大化按钮_hover_57_40.png",
                    "pressed": ":/images/title_bar/黑色最大化按钮_pressed_57_40.png",
                },
                {
                    "normal": ":/images/title_bar/白色最大化按钮_57_40.png",
                    "hover": ":/images/title_bar/绿色最大化按钮_hover_57_40.png",
                    "pressed": ":/images/title_bar/黑色最大化按钮_pressed_57_40.png",
                },
            ],
            [
                {
                    "normal": ":/images/title_bar/黑色向下还原按钮_57_40.png",
                    "hover": ":/images/title_bar/绿色向下还原按钮_hover_57_40.png",
                    "pressed": ":/images/title_bar/向下还原按钮_pressed_57_40.png",
                },
                {
                    "normal": ":/images/title_bar/白色向下还原按钮_57_40.png",
                    "hover": ":/images/title_bar/绿色向下还原按钮_hover_57_40.png",
                    "pressed": ":/images/title_bar/向下还原按钮_pressed_57_40.png",
                },
            ],
        ]
        self.resize(57, 40)
        # 设置标志位
        self.isMax = False
        self.isWhiteIcon = False
        self.setStyleSheet("QPushButton{border:none;margin:0}")
        self.setIcon(
            QIcon(":/images/title_bar/透明黑色最大化按钮_57_40.png"))
        self.setIconSize(QSize(57, 40))

    def setWhiteIcon(self, isWhite: bool):
        """ 设置图标颜色 """
        self.isWhiteIcon = isWhite
        self.__updateIcon("normal")

    def __updateIcon(self, iconState: str):
        """ 更新图标 """
        self.setIcon(
            QIcon(self.iconPathDict_list[self.isMax]
                  [self.isWhiteIcon][iconState])
        )

    def enterEvent(self, e):
        """ hover时更换图标 """
        self.__updateIcon("hover")

    def leaveEvent(self, e):
        """ leave时更换图标 """
        self.__updateIcon("normal")

    def mousePressEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.__updateIcon("pressed")
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """ 鼠标松开时更换按钮图标 """
        if e.button() == Qt.RightButton:
            return
        self.isMax = not self.isMax
        self.__updateIcon("normal")
        super().mouseReleaseEvent(e)

    def setMaxState(self, isMax: bool):
        """ 更新最大化标志位和图标 """
        if self.isMax == isMax:
            return
        self.isMax = isMax
        self.__updateIcon("normal")
