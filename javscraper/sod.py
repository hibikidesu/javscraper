from abc import ABC
from typing import Optional

from urllib.parse import quote
from .base import Base

import requests

__all__ = ["SOD"]


class SOD(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://ec.sod.co.jp")
        self._set_date_fmt("%Y年 %m月 %d日")
        self._set_fail_callback(self._fail_callback)
        self._set_allow_redirects(True)
        self._set_search_xpath("//div[@class='videis_s_txt']//a")
        self._set_video_xpath({
            "name": "//div[@id='videos_head']/h1",
            "code": "//table[@id='v_introduction']/tr[contains(td, '品番')]/td[@class='v_intr_tx']",
            "studio": "//table[@id='v_introduction']/tr[contains(td, 'メーカー')]/td[@class='v_intr_tx']",
            "image": self._fix_image,
            "actresses": "//table[@id='v_introduction']/tr[contains(td, '出演者')]/td[@class='v_intr_tx']//a",
            "genres": "//table[@id='v_introduction']/tr[contains(td, 'ジャンル')]/td[@class='v_intr_tx']//a",
            "release_date": "//table[@id='v_introduction']/tr[contains(td, '発売年月日')]"
                            "/td[@class='v_intr_tx']",
            "description": "//article"
        })

    def _build_search_path(self, query: str) -> str:
        self._set_headers({
            "Referer": f"{self.PARAMS['base_url']}/prime/videos/genre/"
                       f"?search_type=1&sodsearch={quote(query)}"
        })
        return "/prime/_ontime.php"

    def _build_video_path(self, query: str) -> Optional[str]:
        self._set_headers({
            "Referer": f"{self.PARAMS['base_url']}/prime/videos/?id={quote(query)}"
        })
        return "https://ec.sod.co.jp/prime/_ontime.php"

    @staticmethod
    def _fail_callback(result):
        if result.url == "https://ec.sod.co.jp/prime/":
            raise ValueError()

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return tree.xpath("//div[@class='videos_samimg']/a")[0].get("href")

    @staticmethod
    def download_image(url: str) -> requests.Response:
        """
        Downloads an image which will normally 403 without referrer header
        :param url: URL to download from cloudfront
        :return: HTTP Response
        """
        return requests.get(url, headers={"Referer": "https://ec.sod.co.jp/"})
