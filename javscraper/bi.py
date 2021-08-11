from abc import ABC
from typing import Optional

import re
from urllib.parse import quote, urljoin
from .base import Base
from .utils import fix_jav_code

__all__ = ["Bi"]


class Bi(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.bi-av.com")
        self._set_date_fmt("%Y年%m月%d日")
        self._set_search_xpath("//a[@class='img-works-list-item']")
        self._set_video_xpath({
            "name": "//div[@class='hd-ttl']/h1",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//dl[@class='bx-titledata']/dd[1]/div/a",
            "genres": "//dl[@class='bx-titledata']/dd[8]/a",
            "release_date": "//dl[@class='bx-titledata']/dd[3]/a",
            "description": "//dl[@class='bx-titledata']/dd[2]/p",
            "sample_video": self._fix_sample_video
        })

    def _build_search_path(self, query: str) -> str:
        path = f"/search/list/?q={quote(query)}"
        return path

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        code = re.search(r"/detail/([a-zA-Z0-9-_]*)", url).group(1)
        return fix_jav_code(code)

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "Bi"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return urljoin(url, tree.xpath("//a[contains(@class, 'cboxElement')]")[0].get("href"))

    @staticmethod
    def _fix_sample_video(url: str, tree) -> Optional[str]:
        video = tree.xpath("//div[@id='js-c-box-video']/video")
        if not video:
            return None
        return video[0].get("src")
