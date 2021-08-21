from abc import ABC
from typing import Optional

import re
from urllib.parse import quote
from .base import Base

__all__ = ["Heyzo"]


class Heyzo(Base, ABC):

    def __init__(self, english: bool = False):
        """
        :param english: Result language
        """
        if english:
            base = "https://en.heyzo.com"
        else:
            base = "https://www.heyzo.com"

        super().__init__(base_url=base)
        self._set_date_fmt("%Y-%m-%d")
        self._set_search_xpath("//div[@id='movies']//div[contains(@class, 'movie')]/a[1]")
        self._set_video_xpath({
            "name": self._fix_name,
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//table[@class = 'movieInfo']/tbody/tr[2]/td[2]//a",
            "genres": self._fix_genres,
            "release_date": "//table[@class = 'movieInfo']/tbody/tr[1]/td[2]",
            "description": "//p[@class = 'memo']"
        })

    def _build_search_path(self, query: str) -> str:
        return f"/search/{quote(query)}/1.html?&sort=pop"

    def _build_video_path(self, query: str) -> Optional[str]:
        query = query.lower().replace("heyzo-", "")
        return f"{self.PARAMS['base_url']}/moviepages/{query}/index.html"

    @staticmethod
    def _fix_name(url: str, tree) -> str:
        # Remove actress from title
        return tree.xpath("//div[@id='movie']/h1[1]")[0].text_content().rpartition("-")[0].strip()

    @staticmethod
    def _get_code(url: str):
        return  re.search(r"moviepages/([0-9-]*)", url).group(1)

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        return "Heyzo-" + Heyzo._get_code(url)

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "Heyzo"

    @staticmethod
    def _fix_genres(url: str, tree) -> list:
        if "en.heyzo" in url:
            return [
                x.text_content().strip() for x in
                tree.xpath("//table[@class = 'movieInfo']/tbody/tr[6]/td[2]//a")
            ]
        else:
            return [
                x.text_content().strip() for x in
                tree.xpath("//table[@class = 'movieInfo']/tbody/tr[7]//a")
            ]

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        code = Heyzo._get_code(url)
        return f"https://en.heyzo.com/contents/3000/{code}/images/player_thumbnail_en.jpg"
