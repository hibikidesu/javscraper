from abc import ABC
from typing import Optional

from urllib.parse import quote, urljoin
from .base import Base

__all__ = ["KMProduce"]


class KMProduce(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.km-produce.com")
        self._set_date_fmt("%Y/%m/%d")
        self._set_cookies({"modal": "off"})
        self._set_search_xpath("//article[@class='post']/h3/a")
        self._set_video_xpath({
            "name": "//div[@class='pagettl']/h1",
            "code": "//dl[@class='second']/dd[2]",
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": self._fix_actresses,
            "genres": "//dl[@class='first']/dd[4]//a",
            "release_date": "//dl[@class='second']/dd[1]",
            "description": "//p[@class='intro']",
            "sample_video": self._fix_sample_video
        })

    def _build_search_path(self, query: str) -> str:
        return f"/?s={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        return f"{self.PARAMS['base_url']}/works/{quote(query)}"

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "K.M.Produce"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return urljoin(url, tree.xpath("//p[@id='fulljk']/a")[0].get("href"))

    @staticmethod
    def _fix_actresses(url: str, tree) -> list:
        actresses = tree.xpath("//dd[@class='act']//span")
        return [x.text_content() for x in actresses]

    @staticmethod
    def _fix_sample_video(url: str, tree) -> Optional[str]:
        mov = tree.xpath("//div[@class='mov']/a")
        if not mov:
            return None
        return mov[0].get("href")
