from abc import ABC
from typing import Optional

import re
from lxml import etree
from datetime import datetime
from urllib.parse import quote, urljoin
from .base import Base
from .utils import fix_jav_code

__all__ = ["Attackers"]


class Attackers(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.attackers.net")
        self._set_date_fmt("%Y年%m月%d日")
        self._set_search_xpath("//a[@class='works-list-item-info']")
        self._set_video_xpath({
            "name": "//h2[@class='page-sub-title-tx']",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//ul[@class='works-detail-info']/li/dl[contains(dt, '出演女優')]/dd//a",
            "genres": "//ul[@class='works-detail-info']/li/dl[contains(dt, 'ジャンル')]/dd//a",
            "release_date": "//ul[@class='works-detail-info']/li/dl[contains(dt, '発売日')]/dd//a",
            "description": "//div[@class='works-detail-desc-tx']/p"
        })

    def _build_search_path(self, query: str) -> str:
        return f"/search/list/?q={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "Attackers"

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        code = tree.xpath("//ul[@class='works-detail-info']/li/dl[contains(dt, '品番')]//li[1]/text()")[1]
        return fix_jav_code(code.strip())

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return urljoin(url, tree.xpath("//figure[1]/a")[0].get("href"))

    @staticmethod
    def _fix_release_date(url: str, tree) -> datetime:
        date = tree.xpath("//dl[@class='lst-works-data' and contains(dt, '発売日')]/dd//a")[0].get("href")
        date = re.search(r"/([0-9]*)/", date).group(1)
        return datetime.strptime(date, "%Y%m%d")
