from abc import ABC
from typing import Optional

from urllib.parse import quote
from .base import Base
from .utils import SCRAPER

__all__ = ["AuroraProject"]


class AuroraProject(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://sec.aurora-pro.com")
        self._set_allow_redirects(True)
        self._set_date_fmt("%Y/%m/%d")
        self._set_search_xpath("//div[@id='searchResultPkg']/dl/dt[1]/a")
        self._set_video_xpath({
            "name": "//h1[@class='pro_title']",
            "code": "//div[@id='product_info']/dl/dd[2]//li[1]",
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//div[@id='product_info']/dl/dd[1]//a",
            "genres": self._fix_genres,
            "release_date": "//div[@id='product_info']/dl/dd[5]",
            "description": "//div[@id='product_exp']/p"
        })

    def _build_search_path(self, query: str) -> str:
        path = f"/other/list.html?type=2&area=other&srch={quote(query)}&answer_yes=1"
        SCRAPER.get(self.PARAMS["base_url"] + path).close()
        return path

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "Aurora Project Annex"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return tree.xpath("//img[@id='main_pkg']")[0].get("src")

    @staticmethod
    def _fix_genres(url: str, tree) -> list:
        genres = [x.text_content() for x in tree.xpath("//div[@id='product_info']/dl/dd[6]//a")]
        f_type = [x.text_content() for x in tree.xpath("//div[@id='product_info']/dl/dd[7]//a")]
        scenes = [x.text_content() for x in tree.xpath("//div[@id='product_info']/dl/dd[8]//a")]
        return genres + f_type + scenes
