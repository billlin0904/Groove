# coding:utf-8
from components.widgets.selection_mode_bar_base import (BasicButton,
                                                        SelectionModeBarBase,
                                                        CheckAllButton)


class SelectionModeBar(SelectionModeBarBase):
    """ 选择模式栏 """

    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建按钮
        self.__createButtons()
        # 初始化界面
        self.__initWidget()

    def __createButtons(self):
        """ 创建按钮 """
        self.cancelButton = BasicButton(
            ":/images/selection_mode_bar/Cancel.png", self.tr("Cancel"), self)
        self.playButton = BasicButton(
            ":/images/selection_mode_bar/Play.png", self.tr("Play"), self)
        self.nextToPlayButton = BasicButton(
            ":/images/selection_mode_bar/NextToPlay.png", self.tr("Play next"), self)
        self.showAlbumButton = BasicButton(
            ":/images/selection_mode_bar/ShowAlbum.png", self.tr("Show album"), self)
        self.addToButton = BasicButton(
            ":/images/selection_mode_bar/Add.png", self.tr("Add to"), self)
        self.editInfoButton = BasicButton(
            ":/images/selection_mode_bar/Edit.png", self.tr("Edit info"), self)
        self.propertyButton = BasicButton(
            ":/images/selection_mode_bar/Property.png", self.tr("Properties"), self)
        self.deleteButton = BasicButton(
            ":/images/selection_mode_bar/Delete.png", self.tr("Delete"), self)
        self.checkAllButton = CheckAllButton(
            [
                ":/images/selection_mode_bar/SelectAll.png",
                ":/images/selection_mode_bar/CancelSelectAll.png",
            ],
            [self.tr("Select all"), self.tr("Deselect all")],
            self,
        )

    def __initWidget(self):
        """ 初始化界面 """
        self.addButtons([
            self.cancelButton, self.playButton, self.nextToPlayButton,
            self.addToButton, self.showAlbumButton, self.editInfoButton,
            self.propertyButton, self.deleteButton, self.checkAllButton
        ])
        self.setToHideButtons(self.button_list[4:-2])
        self.insertSeparator(1)
