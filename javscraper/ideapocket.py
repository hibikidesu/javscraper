from abc import ABC
from typing import Optional

import re
from urllib.parse import quote
from .base import Base
from .utils import fix_jav_code

__all__ = ["IdeaPocket"]


class IdeaPocket(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.ideapocket.com")
        self._set_date_fmt("%Y年%m月%d日")
        self._set_search_xpath("//a[@class='img hover']")
        self._set_video_xpath({
            "name": "//h2[@class='p-workPage__title']",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//div[@class='p-workPage__table']/div[@class='item']/div[contains(text(), '女優')]/../div[2]//a",
            "genres": "//div[@class='p-workPage__table']/div[@class='item']/div[contains(text(), 'ジャンル')]/../div[2]//a",
            "release_date": "//div[@class='p-workPage__table']/div[@class='item']/div[contains(text(), '発売日')]/../div[2]//a",
            "description": "//p[@class='p-workPage__text']",
            "sample_video": self._fix_sample_video
        })
        self._set_allow_redirects(True)

    def _build_search_path(self, query: str) -> str:
        query = query.replace("-", "")
        return f"/search/list/?keyword={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _get_raw_code(url):
        return re.search(r"/detail/([a-zA-Z0-9_]*)", url).group(1)

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        code = tree.xpath("//div[@class='p-workPage__table']/div[@class='item']/div[contains(text(), '品番')]/../div[2]//p/text()")[0]
        return fix_jav_code(code.replace("DVD", "", 1).strip())

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "IdeaPocket"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        path = tree.xpath("//div[@class='swiper-slide'][1]/img/@data-src")[0]
        return path

    @staticmethod
    def _fix_sample_video(url: str, tree) -> str:
        return tree.xpath("//video")[0].get("src")
