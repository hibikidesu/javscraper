from abc import ABC
from typing import Optional

from urllib.parse import quote
from .base import Base

__all__ = ["MaxA"]


class MaxA(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.max-a.co.jp")
        self._set_date_fmt("%Y年%m月%d日")
        self._set_search_xpath("//dd[contains(@class, 'description')]/ul/li[1]/a")
        self._set_video_xpath({
            "name": "//div[@class='columnHeading']/h2",
            "code": "//div[@class='description']/dl[contains(dt, '商品番号')]/dd",
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//div[@class='description']/dl[contains(dt, '女優名')]/dd/a",
            "genres": "//dl[@class='option']//a",
            "release_date": "//div[@class='description']/dl[contains(dt, '発売日')]/dd",
            "description": "//dd[@class='reviewTxt']"
        })

    def _build_search_path(self, query: str) -> str:
        return f"/search_item.php" \
               f"?search=t" \
               f"&word_type=download_only" \
               f"&word={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "MAX-A"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return tree.xpath("//a[@class='thickbox']")[0].get("href")
