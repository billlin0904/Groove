# coding:utf-8
from fuzzywuzzy import fuzz
from common.crawler import KuWoMusicCrawler, WanYiMusicCrawler, KuGouMusicCrawler
from PyQt5.QtCore import pyqtSignal, QThread


class GetMvUrlThread(QThread):
    """ 获取 MV 播放地址线程 """

    crawlFinished = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.key_word = ''
        self.video_quality = 'Full HD'
        self.crawlers = [
            KuGouMusicCrawler(),
            WanYiMusicCrawler(),
            KuWoMusicCrawler()
        ]

    def run(self):
        url = ''
        for crawler in self.crawlers:
            mvInfo_list, _ = crawler.getMvInfoList(self.key_word, page_size=10)
            if not mvInfo_list:
                continue

            # 匹配搜索结果
            matches = [fuzz.token_set_ratio(
                i['singer']+' '+i['name'], self.key_word) for i in mvInfo_list]
            best_match = max(matches)
            if best_match < 90:
                continue

            url = crawler.getMvUrl(
                mvInfo_list[matches.index(best_match)], self.video_quality)
            if url:
                break

        self.crawlFinished.emit(url)

    def setVideoQuality(self, quality: str):
        """ 设置视频的画质 """
        self.video_quality = quality
