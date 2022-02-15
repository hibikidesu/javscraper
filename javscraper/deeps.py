from abc import ABC
from typing import Optional

import re
from urllib.parse import quote
from .base import Base
from .utils import fix_jav_code

__all__ = ["Deeps"]


class Deeps(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://deeps.net")
        self._set_date_fmt("%Y.%m.%d")
        self._set_search_xpath("//li[@class='ippan']/a[1]")
        self._set_video_xpath({
            "name": "//h1[@class='ippan']",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//table[@class='t3']/tbody/tr[contains(th, '出演')]/td",
            "genres": self._fix_genres,
            "release_date": "//table[@class='t1']/tbody/tr[contains(th, '発売日')]/td",
            "sample_video": self._fix_sample_video
        })

    def _build_search_path(self, query: str) -> str:
        path = f"/item/?search={quote(query)}"
        return path

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "Deeps"

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        code = re.search(r"/product/([a-zA-Z0-9-_]*)", url).group(1)
        return fix_jav_code(code)

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return tree.xpath("//img[@class='pc']")[0].get("src")

    @staticmethod
    def _fix_genres(url: str, tree) -> list:
        genres = [x.text_content() for x in tree.xpath("//table[@class='t3']/tbody/tr[contains(th, 'カテゴリ')]/td/a")]
        f_type = [x.text_content() for x in tree.xpath("//table[@class='t3']/tbody/tr[contains(th, 'タイプ')]/td/a")]
        return genres + f_type

    @staticmethod
    def _fix_sample_video(url: str, tree) -> Optional[str]:
        video = tree.xpath("//div[@class='wrap-video']/video/source")
        if not video:
            return None
        return video[0].get("src")
