from abc import ABC
from typing import Optional

from urllib.parse import quote, urljoin
from .base import Base
from .utils import fix_jav_code

__all__ = ["AirControl"]


class AirControl(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.i-dol.tv")
        self._set_date_fmt("%Y年%m月%d日")
        self._set_search_xpath("//div[@class='c-works-list-item']/div/a")
        self._set_video_xpath({
            "name": "//dd[@class='works-info-main-ttl']/h1",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//div[@class='works-info']/dl[contains(dt, '出演')]/dd//a",
            "genres": "//div[@class='works-info']/dl[contains(dt, 'ジャンル')]/dd//a",
            "release_date": "//div[@class='works-info']/dl[contains(dt, '発売日')]/dd//a",
            "description": "//div[@class='works-info-comment']/p",
            "sample_video": self._fix_sample_video
        })

    def _build_search_path(self, query: str) -> str:
        return f"/search/list/?q={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        code = tree.xpath("//div[@class='works-info']/dl[contains(dt, '品番')]/dd/span[1]/text()")[0]
        return fix_jav_code(code)

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "Air Control"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return urljoin(url, tree.xpath("//figure/a")[0].get("href"))

    @staticmethod
    def _fix_sample_video(url: str, tree) -> Optional[str]:
        video = tree.xpath("//video")
        if not video:
            return None
        return video[0].get("src")
