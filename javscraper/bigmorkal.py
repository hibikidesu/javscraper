from abc import ABC
from typing import Optional

from urllib.parse import quote
from .base import Base

__all__ = ["BigMorkal"]


class BigMorkal(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://bigmorkal.co.jp")
        self._set_cookies({"age_gate": "18"})
        self._set_date_fmt("%Y-%m-%d")
        self._set_search_xpath("//article/a[1]")
        self._set_video_xpath({
            "name": "//h1[@class='p-entry__header02-title']",
            "code": "//table[@class='details']/tr[contains(th, '品　　番')]/td",
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//table[@class='details']/tr[contains(th, '出演者')]/td/a",
            "genres": "//table[@class='details']/tr[contains(th, 'ジャンル')]/td/a",
            "release_date": "//table[@class='details']/tr[contains(th, '公開日')]/td/a",
            "description": "//table[@class='details']/tr[contains(th, '内　　容')]/td"
        })

    def _build_search_path(self, query: str) -> str:
        path = f"/?s={quote(query)}"
        return path

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "BIGMORKAL"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return tree.xpath("//img[contains(@class, 'size-full')]")[0].get("src")
