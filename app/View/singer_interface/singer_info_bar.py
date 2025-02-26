# coding:utf-8
import os
from pathlib import Path

from components.widgets.menu import AddToMenu
from common.image_process_utils import getBlurPixmap
from components.app_bar import AppBarButton, CollapsingAppBarBase, MoreActionsMenu
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QObject
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtWidgets import QLabel, QAction


class SingerInfoBar(CollapsingAppBarBase):
    """ 歌手信息栏 """

    defaultCoverPath = ':/images/default_covers/singer_295_295.png'

    addSongsToPlayingPlaylistSig = pyqtSignal()
    addSongsToNewCustomPlaylistSig = pyqtSignal()
    addSongsToCustomPlaylistSig = pyqtSignal(str)

    def __init__(self, singerInfo: dict, parent=None):
        self.__getInfo(singerInfo)
        super().__init__(self.singer, self.genre, self.coverPath, 'singer', parent)

        # 创建按钮
        self.playAllButton = AppBarButton(
            ":/images/album_interface/Play.png", self.tr("Play all"))
        self.addToButton = AppBarButton(
            ":/images/album_interface/Add.png", self.tr("Add to"))
        self.pinToStartMenuButton = AppBarButton(
            ":/images/album_interface/Pin.png", self.tr('Pin to Start'))
        self.setButtons([self.playAllButton, self.addToButton,
                        self.pinToStartMenuButton])

        self.blurLabel = BlurLabel(self.coverPath, 8, self)
        self.blurLabel.lower()
        self.blurLabel.setHidden(self.coverPath == self.defaultCoverPath)

        self.actionNames = [
            self.tr("Play all"), self.tr("Add to"), self.tr('Pin to Start')]
        self.action_list = [QAction(i, self) for i in self.actionNames]
        self.addToButton.clicked.connect(self.__onAddToButtonClicked)

        self.setAttribute(Qt.WA_StyledBackground)
        self.setAutoFillBackground(True)

    def __getInfo(self, singerInfo: dict):
        """ 获取信息 """
        obj = QObject()
        self.singer = singerInfo.get('singer', obj.tr('Unknown artist'))
        self.genre = singerInfo.get('genre', obj.tr('Unknown genre'))
        self.albumInfo_list = singerInfo.get('albumInfo_list', [])

        # 获取歌手头像
        avatars = {i.stem: i for i in Path('cache/singer_avatar').glob('*')}
        self.coverPath = str(avatars.get(self.singer, self.defaultCoverPath))

    def setBackgroundColor(self):
        """ 根据封面背景颜色 """
        if self.coverPath == self.defaultCoverPath:
            palette = QPalette()
            palette.setColor(self.backgroundRole(), QColor(24, 24, 24))
            self.setPalette(palette)

        if hasattr(self, 'blurLabel'):
            self.blurLabel.setHidden(self.coverPath == self.defaultCoverPath)

    def updateWindow(self, singerInfo: dict):
        self.__getInfo(singerInfo)
        self.updateCover(self.coverPath)
        super().updateWindow(self.singer, self.genre, self.coverPath)

    def updateCover(self, coverPath: str):
        """ 更新封面 """
        self.coverLabel.setPixmap(QPixmap(coverPath))
        self.blurLabel.updateWindow(coverPath, 8)
        self.__adjustBlurLabel()
        self.blurLabel.show()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.__adjustBlurLabel()

    def __adjustBlurLabel(self):
        """ 调整磨砂封面 """
        w = max(self.width(), self.height())
        self.blurLabel.resize(self.width(), self.height())
        self.blurLabel.setPixmap(self.blurLabel.pixmap().scaled(
            w, w, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def onMoreActionsButtonClicked(self):
        """ 显示更多操作菜单 """
        menu = MoreActionsMenu()
        index = len(self.buttons)-self.hiddenButtonNum
        actions = self.action_list[index:]
        menu.addActions(actions)
        pos = self.mapToGlobal(self.moreActionsButton.pos())
        x = pos.x()+self.moreActionsButton.width()+5
        y = pos.y()+self.moreActionsButton.height()//2-(13+38*len(actions))//2
        menu.exec(QPoint(x, y))

    def __onAddToButtonClicked(self):
        """ 显示添加到菜单 """
        menu = AddToMenu(parent=self)
        pos = self.mapToGlobal(self.addToButton.pos())
        x = pos.x() + self.addToButton.width() + 5
        y = pos.y() + self.addToButton.height() // 2 - \
            (13 + 38 * menu.actionCount()) // 2
        menu.playingAct.triggered.connect(self.addSongsToPlayingPlaylistSig)
        menu.addSongsToPlaylistSig.connect(self.addSongsToCustomPlaylistSig)
        menu.newPlaylistAct.triggered.connect(
            self.addSongsToNewCustomPlaylistSig)
        menu.exec(QPoint(x, y))


class BlurLabel(QLabel):
    """ 磨砂标签 """

    def __init__(self, imagePath: str, blurRadius=30, parent=None):
        super().__init__(parent=parent)
        self.imagePath = imagePath
        self.blurRadius = blurRadius
        self.setPixmap(getBlurPixmap(imagePath, blurRadius, 0.85))

    def updateWindow(self, imagePath: str, blurRadius=30):
        """ 更新磨砂图片 """
        self.imagePath = imagePath
        self.blurRadius = blurRadius
        self.setPixmap(getBlurPixmap(imagePath, blurRadius, 0.85, (450, 450)))
