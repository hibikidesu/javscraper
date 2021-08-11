from abc import ABC
from typing import Optional

import re
from datetime import datetime
from urllib.parse import quote, urljoin
from .base import Base

__all__ = ["Aroma"]


class Aroma(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.aroma-p.com")
        self._set_search_xpath("//div[@class='wrap-works-item']/a")
        self._set_video_xpath({
            "name": "//p[@class='ttl-main-works-package']",
            "code": "//dl[@class='lst-works-data' and contains(dt, '品番')]/dd",
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//dl[@class='lst-works-data' and contains(dt, '出演者')]/dd//li[@class='item-works-cast']",
            "genres": "//dl[@class='lst-works-data' and contains(dt, 'ジャンル')]/dd//a",
            "release_date": self._fix_release_date,
            "description": "//p[@class='tx-works-info']",
            "sample_video": self._fix_sample_video
        })

    def _build_search_path(self, query: str) -> str:
        return f"/search/list/?q={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        return f"https://www.aroma-p.com/works/detail/{query.replace('-', '')}/"

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "Aroma Kikaku"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return urljoin(url, tree.xpath("//div[@class='img-main-works-package']/img")[0].get("src"))

    @staticmethod
    def _fix_release_date(url: str, tree) -> datetime:
        date = tree.xpath("//dl[@class='lst-works-data' and contains(dt, '発売日')]/dd//a")[0].get("href")
        date = re.search(r"/([0-9]*)/", date).group(1)
        return datetime.strptime(date, "%Y%m%d")

    @staticmethod
    def _fix_sample_video(url: str, tree) -> Optional[str]:
        video = tree.xpath("//a[@rel='sample_movie']")
        if not video:
            return None
        return video[0].get("data-movie-path")
