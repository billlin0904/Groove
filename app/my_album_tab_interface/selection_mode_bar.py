# coding:utf-8

from app.my_widget.basic_selection_mode_bar import (BasicButton,
                                                    BasicSelectionModeBar,
                                                    CheckAllButton)


class SelectionModeBar(BasicSelectionModeBar):
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
            r'app\resource\images\selection_mode_bar\取消_20_20.png', '取消', self)
        self.playButton = BasicButton(
            r'app\resource\images\selection_mode_bar\播放_20_20.png', '播放', self)
        self.nextToPlayButton = BasicButton(
            r'app\resource\images\selection_mode_bar\下一首播放_20_20.png', '下一首播放', self)
        self.addToButton = BasicButton(
            r'app\resource\images\selection_mode_bar\添加到_20_20.png', '添加到', self)
        self.showSongerButton = BasicButton(
            r'app\resource\images\selection_mode_bar\显示歌手_20_20.png', '显示歌手', self)
        self.editInfoButton = BasicButton(
            r'app\resource\images\selection_mode_bar\编辑信息_20_20.png', '编辑信息', self)
        self.pinToStartMenuButton = BasicButton(
            r'app\resource\images\selection_mode_bar\固定到开始菜单_20_20.png', '固定到"开始"菜单', self)
        self.deleteButton = BasicButton(
            r'app\resource\images\selection_mode_bar\删除_20_20.png', '删除', self)
        self.checkAllButton = CheckAllButton(
            [r'app\resource\images\selection_mode_bar\全选_20_20.png',
             r'app\resource\images\selection_mode_bar\取消全选_20_20.png'], ['全选', '取消全选'], self)

    def __initWidget(self):
        """ 初始化界面 """
        self.addButtons([self.cancelButton, self.playButton, self.nextToPlayButton,
                         self.addToButton, self.showSongerButton, self.pinToStartMenuButton,
                         self.editInfoButton, self.deleteButton, self.checkAllButton])
        self.setToHideButtons(self.button_list[4:-2])
        self.insertSeparator(1)


