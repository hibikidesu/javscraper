from abc import ABC
from typing import Optional

import re
from urllib.parse import quote
from .base import Base
from .utils import fix_jav_code

__all__ = ["S1"]


class S1(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://s1s1s1.com")
        self._set_date_fmt("%Y年%m月%d日")
        self._set_fail_callback(self._fail_callback)
        self._set_search_xpath("//div[@class='c-card']/a")
        self._set_video_xpath({
            "name": "//h2[@class='p-workPage__title']",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//div[@class='item' and contains(div, '女優')]//a",
            "genres": "//div[@class='item' and contains(div, 'ジャンル')]//a",
            "release_date": "//div[@class='item' and contains(div, '発売日')]//a",
            "description": "//p[@class='p-workPage__text']",
            "sample_video": self._fix_sample_video
        })

    def _build_search_path(self, query: str) -> str:
        return f"/search/list?keyword={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        query = query.replace('-', '').strip()
        return f"{self.PARAMS['base_url']}/works/detail/{query}"

    @staticmethod
    def _fail_callback(result):
        if b"404 Not Found" in result.content:
            raise ValueError()

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        value = re.search(r"detail/([a-zA-Z0-9]*)", url).group(1)
        return fix_jav_code(value)

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "S1 NO.1 STYLE"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        path = tree.xpath("//div[@class='swiper-slide'][1]/img/@data-src")[0]
        return path

    @staticmethod
    def _fix_sample_video(url: str, tree) -> str:
        return tree.xpath("//video")[0].get("src")
