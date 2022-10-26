from abc import ABC
from typing import Optional

import re
from urllib.parse import quote, urljoin
from .base import Base
from .utils import fix_jav_code

__all__ = ["Bi"]


class Bi(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://bi-av.com")
        self._set_date_fmt("%Y年%m月%d日")
        self._set_search_xpath("//div[@class='c-card']//a")
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

    def _build_search_path(self, query: str) -> str:
        path = f"/search/list?keyword={quote(query.replace('-', ''))}"
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
        return tree.xpath("//div[@class='swiper-slide']//img")[0].get("data-src")

    @staticmethod
    def _fix_sample_video(url: str, tree) -> Optional[str]:
        video = tree.xpath("//div[@class='video']/video")
        if not video:
            return None
        return video[0].get("src")
