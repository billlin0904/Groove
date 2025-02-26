# coding:utf-8
from components.widgets.menu import AddToMenu, DWMMenu
from components.song_list_widget import NoScrollSongListWidget, SongCardType
from PyQt5.QtCore import pyqtSignal, QFile
from PyQt5.QtGui import QContextMenuEvent
from PyQt5.QtWidgets import QAction


class SongListWidget(NoScrollSongListWidget):
    """ 歌曲卡列表视图 """

    playSignal = pyqtSignal(int)                        # 将当前歌曲切换为指定的歌曲卡
    playOneSongSig = pyqtSignal(dict)                   # 只播放一首歌
    nextToPlayOneSongSig = pyqtSignal(dict)             # 下一首播放
    switchToSingerInterfaceSig = pyqtSignal(str)        # 切换到歌手界面
    switchToAlbumInterfaceSig = pyqtSignal(str, str)    # 切换到专辑界面

    def __init__(self, songInfo_list: list, parent):
        """
        Parameters
        ----------
        songInfo_list:list
            歌曲信息列表

        parent:
            父级窗口
        """
        super().__init__(songInfo_list, SongCardType.PLAYLIST_INTERFACE_SONG_CARD, parent)
        self.resize(1150, 758)
        self.createSongCards()
        self.__setQss()

    def contextMenuEvent(self, e: QContextMenuEvent):
        """ 重写鼠标右击时间的响应函数 """
        hitIndex = self.indexAt(e.pos()).column()
        # 显示右击菜单
        if hitIndex > -1:
            contextMenu = SongCardListContextMenu(self)
            self.__connectMenuSignalToSlot(contextMenu)
            contextMenu.exec(self.cursor().pos())

    def __setQss(self):
        """ 设置层叠样式 """
        f = QFile(":/qss/song_tab_interface_song_list_widget.qss")
        f.open(QFile.ReadOnly)
        self.setStyleSheet(str(f.readAll(), encoding='utf-8'))
        f.close()

    def __onPlayButtonClicked(self, index):
        """ 歌曲卡播放按钮槽函数 """
        self.playSignal.emit(index)
        self.setCurrentIndex(index)
        self.setPlay(index)

    def __onSongCardDoubleClicked(self, index):
        """ 发送当前播放的歌曲卡变化信号，同时更新样式和歌曲信息卡 """
        if self.isInSelectionMode:
            return
        self.playSignal.emit(index)

    def __onRemoveButtonClicked(self, index, songCard=None):
        """ 移除歌曲卡按钮点击槽函数 """
        path = songCard.songPath if songCard else self.sender().songPath
        self.removeSongCard(index)
        self.removeSongSignal.emit(path)

    def _connectSongCardSignalToSlot(self, songCard):
        """ 将歌曲卡信号连接到槽 """
        songCard.doubleClicked.connect(self.__onSongCardDoubleClicked)
        songCard.removeSongSignal.connect(self.__onRemoveButtonClicked)
        songCard.playButtonClicked.connect(self.__onPlayButtonClicked)
        songCard.clicked.connect(self.setCurrentIndex)
        songCard.checkedStateChanged.connect(
            self.onSongCardCheckedStateChanged)
        songCard.switchToAlbumInterfaceSig.connect(
            self.switchToAlbumInterfaceSig)
        songCard.switchToSingerInterfaceSig.connect(
            self.switchToSingerInterfaceSig)

    def __connectMenuSignalToSlot(self, menu):
        """ 右击菜单信号连接到槽 """
        menu.playAct.triggered.connect(
            lambda: self.playOneSongSig.emit(
                self.songCard_list[self.currentRow()].songInfo))
        menu.nextSongAct.triggered.connect(
            lambda: self.nextToPlayOneSongSig.emit(
                self.songCard_list[self.currentRow()].songInfo))
        menu.editInfoAct.triggered.connect(self.showSongInfoEditDialog)
        menu.showPropertyAct.triggered.connect(
            self.showSongPropertyDialog)
        menu.deleteAct.triggered.connect(lambda: self.__onRemoveButtonClicked(
            self.currentRow(), self.songCard_list[self.currentRow()]))
        menu.selectAct.triggered.connect(
            lambda: self.songCard_list[self.currentRow()].setChecked(True))
        menu.showAlbumAct.triggered.connect(lambda: self.switchToAlbumInterfaceSig.emit(
            self.songCard_list[self.currentRow()].album,
            self.songCard_list[self.currentRow()].singer))

        menu.addToMenu.playingAct.triggered.connect(
            lambda: self.addSongToPlayingSignal.emit(
                self.songCard_list[self.currentRow()].songInfo))
        menu.addToMenu.addSongsToPlaylistSig.connect(
            lambda name: self.addSongsToCustomPlaylistSig.emit(
                name, self.songInfo_list))
        menu.addToMenu.newPlaylistAct.triggered.connect(
            lambda: self.addSongsToNewCustomPlaylistSig.emit(
                [self.songCard_list[self.currentRow()].songInfo]))


class SongCardListContextMenu(DWMMenu):
    """ 歌曲卡列表右击菜单 """

    def __init__(self, parent):
        super().__init__("", parent)
        # 创建主菜单动作
        self.playAct = QAction(self.tr("Play"), self)
        self.nextSongAct = QAction(self.tr("Play next"), self)
        self.deleteAct = QAction(self.tr("Delete from playlist"), self)
        self.showAlbumAct = QAction(self.tr("Show album"), self)
        self.editInfoAct = QAction(self.tr("Edit info"), self)
        self.showPropertyAct = QAction(self.tr("Properties"), self)
        self.selectAct = QAction(self.tr("Select"), self)
        # 创建菜单和子菜单
        self.addToMenu = AddToMenu(self.tr("Add to"), self)
        # 将动作添加到菜单中
        self.addActions([self.playAct, self.nextSongAct])
        # 将子菜单添加到主菜单
        self.addMenu(self.addToMenu)
        # 将其余动作添加到主菜单
        self.addActions([self.deleteAct, self.showAlbumAct,
                        self.editInfoAct, self.showPropertyAct])
        self.addSeparator()
        self.addAction(self.selectAct)
