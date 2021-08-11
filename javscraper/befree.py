from abc import ABC
from typing import Optional

from urllib.parse import quote, urljoin
from .base import Base
from .utils import fix_jav_code

__all__ = ["BeFree"]


class BeFree(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.befreebe.com")
        self._set_date_fmt("%Y年%m月%d日")
        self._set_search_xpath("//a[@class='img-works-list-item']")
        self._set_video_xpath({
            "name": "//h1[@class='c-main-title-with-logo']",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//h2[contains(@class, 'ttl-works-detail-actress')]//a",
            "genres": "//li[@class='item-works-info']/dl[contains(dt, 'ジャンル')]//a",
            "release_date": "//li[@class='item-works-info']/dl[contains(dt, '発売日')]//a",
            "description": "//p[@class='tx-works-comment']",
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
        code = tree.xpath("//li[@class='item-works-info']/dl[contains(dt, '品番')]/dd[1]/text()")[1]
        return fix_jav_code(code.strip())

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "BeFree"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return urljoin(url, tree.xpath("//figure/a")[0].get("href"))

    @staticmethod
    def _fix_sample_video(url: str, tree) -> Optional[str]:
        video = tree.xpath("//div[@id='js-c-box-video']/video")
        if not video:
            return None
        return video[0].get("src")
