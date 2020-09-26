# coding:utf-8

from math import ceil

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout


class GridLayout(QGridLayout):
    """ 可动态调整网格数的网格布局 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__widget_list = []
        self.__rowNum = 0
        self.__columnNum = 0

    def widgets(self) -> list:
        """ 获取布局中的全部部件 """
        return self.__widget_list

    def addWidget(self, widget, row: int, column: int, alignment=Qt.AlignLeft):
        """ 往布局中添加部件 """
        # 只能占用一行一列，否则调整列数时会混乱
        super().addWidget(widget, row, column, 1, 1, alignment)
        self.__widget_list.append(widget)

    def updateColumnNum(self, newColumnNum: int, columnMinWidth: int, rowMinHeight: int):
        """ 调整网格数 """
        newRowNum = ceil(len(self.__widget_list)/newColumnNum)
        currentRowNum = super().rowCount()
        currentColumnNum = super().columnCount()
        self.__columnNum = newColumnNum
        self.__rowNum = newRowNum
        # 先移除所有的小部件
        for widget in self.__widget_list:
            super().removeWidget(widget)
        # 调整网格的宽度和高度
        for col in range(newColumnNum):
            self.setColumnMinimumWidth(col, columnMinWidth)
        for row in range(newRowNum):
            self.setRowMinimumHeight(row, rowMinHeight)
        # 将小部件重新添加到布局中
        for index, widget in enumerate(self.__widget_list):
            x = index // newColumnNum
            y = index - newColumnNum * x
            super().addWidget(widget, x, y, 1, 1, Qt.AlignLeft)
        self.setAlignment(Qt.AlignLeft)
        # 如果现在的总行数小于旧的网格的总行数，就将多出来的行宽度的最小值设为0
        for i in range(currentRowNum - 1, newRowNum-1, -1):
            self.setRowMinimumHeight(i, 0)
        for i in range(currentColumnNum - 1, newColumnNum-1, -1):
            self.setColumnMinimumWidth(i, 0)

    def removeWidget(self, widget):
        """ 从布局中移除一个小部件 """
        super().removeWidget(widget)
        self.__widget_list.remove(widget)

    def removeAllWidgets(self):
        """ 从布局移除所有小部件 """
        for widget in self.__widget_list:
            super().removeWidget(widget)
        self.__widget_list.clear()

    def rowCount(self):
        """ 返回网格行数 """
        return self.__rowNum

    def columnCount(self):
        """ 返回网格列数 """
        return self.__columnNum
