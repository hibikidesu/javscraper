from abc import ABC
from typing import Optional

from urllib.parse import quote
from .base import Base

__all__ = ["AliceJapan"]


class AliceJapan(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.alicejapan.co.jp")
        self._set_cookies({"ageverification": "t"})
        self._set_date_fmt("%Y年%m月%d日")
        self._set_search_xpath("//span[@class='item-title']/..")
        self._set_video_xpath({
            "name": "//div[@class='item-data-title']/h1",
            "code": "//table[@class='mod-item-data-table']/tbody/tr[contains(th, '品番')]/td",
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//table[@class='mod-item-data-table']/tbody/tr[contains(th, '女優名')]/td/a",
            "genres": "//table[@class='mod-item-data-table']/tbody/tr[contains(th, 'ジャンル')]/td/a",
            "release_date": "//table[@class='mod-item-data-table']/tbody/tr[contains(th, '発売日')]/td",
            "description": "//section[@class='item-data-review']/p"
        })

    def _build_search_path(self, query: str) -> str:
        return f"/search_item.php?search=t&word={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "Alice Japan"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return tree.xpath("//a[@class='zoom']")[0].get("href")
