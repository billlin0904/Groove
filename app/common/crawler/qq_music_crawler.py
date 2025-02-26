# coding:utf-8
import json
from typing import Union
from pathlib import Path

import requests
from fuzzywuzzy import fuzz
from .crawler_base import exceptionHandler



class QQMusicCrawler:
    """ QQ 音乐爬虫 """

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    @exceptionHandler()
    def getSongInfo(self, key_word: str, match_thresh=70):
        """ 搜索指定关键词的歌曲信息

        Parameters
        ----------
        key_word: str
            搜索关键词

        match_thresh: int
            匹配度阈值，只返回匹配度大于此阈值的歌曲信息

        Returns
        -------
        song_info: dict
            歌曲信息，如果获取失败返回 `None`
        """
        search_url = f"https://c.y.qq.com/soso/fcgi-bin/client_search_cp?new_json=1&p=1&n=5&w={key_word}"
        response = requests.get(search_url, headers=self.headers)

        infos = json.loads(response.text[9:-1])["data"]["song"]["list"]
        if not infos:
            return None

        # 只取第一个匹配项，只有匹配程度大于 70 才使用该信息
        info = infos[0]
        match_ratio = fuzz.token_set_ratio(
            f"{info['singer'][0]['name']} - {info['name']}", key_word)
        if match_ratio < match_thresh:
            return

        song_info = {}
        song_info["songName"] = info["name"]
        song_info["album"] = info["album"]["name"]
        song_info["year"] = info["time_public"].split('-')[0]
        song_info["singer"] = info["singer"][0]["name"]
        song_info["tracknumber"] = str(info["index_album"])
        song_info["trackTotal"] = str(info["index_album"])
        song_info['disc'] = str(info['index_cd'] + 1)
        song_info['discTotal'] = str(info['index_cd'] + 1)
        song_info["albummid"] = info['album']['mid']

        # 流派信息
        genres = {
            1: 'Pop',
            2: 'classical',
            3: 'Jazz',
            15: 'Blues',
            19: 'Country',
            20: 'Dance',
            21: 'Easy Listening',
            22: 'Rap/Hip Hop',
            23: 'Folk',
            31: 'New Age',
            33: 'R&B/Soul',
            36: 'Rock',
            37: 'Soundtrack',
            39: 'World Music'
        }
        song_info["genre"] = genres.get(info["genre"], 'Pop')

        return song_info

    @exceptionHandler()
    def getAlbumCoverURL(self, albummid: str, save_path: Union[str, Path]):
        """ 获取专辑封面并保存到本地

        Parameters
        ----------
        albummid: str
            专辑 ID，对应 `crawler.getSongInfo(key_word)["albummid"]`

        save_path: str or Path
            本地保存路径

        Returns
        -------
        url: str
            专辑封面 URL，如果没有获取到封面就返回 `None`
        """
        detail_url = f"https://c.y.qq.com/v8/fcg-bin/musicmall.fcg?_=1628997268750&cmd=get_album_buy_page&albummid={albummid}"
        response = requests.get(detail_url, headers=self.headers)
        url = json.loads(response.text[18:-1]
                         )["data"]["headpiclist"][0]["picurl"]

        with open(save_path, 'wb') as f:
            f.write(requests.get(url, headers=self.headers).content)

        return url


