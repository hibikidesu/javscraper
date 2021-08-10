from abc import ABC
from typing import Optional

import re
from urllib.parse import quote
from .base import Base
from .utils import fix_jav_code

__all__ = ["IdeaPocket"]


class IdeaPocket(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.ideapocket.com")
        self._set_date_fmt("%Y年%m月%d日")
        self._set_search_xpath("//a[@class='works-list-item-info']")
        self._set_video_xpath({
            "name": "//div[@class='works-info-ttl']/h1",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//li[contains(@class, 'works-info-data-item') and contains(dl/dt, '女優')]//a",
            "genres": "//li[contains(@class, 'works-info-data-item') and contains(dl/dt, 'ジャンル')]//a",
            "release_date": "//li[contains(@class, 'works-info-data-item') and contains(dl/dt, '発売日')]//a",
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
    def _get_raw_code(url):
        return re.search(r"/detail/([a-zA-Z0-9_]*)", url).group(1)

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        return fix_jav_code(IdeaPocket._get_raw_code(url))

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "IdeaPocket"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        code = IdeaPocket._get_raw_code(url)
        return f"https://www.ideapocket.com/contents/works/{code}/{code}-pl.jpg"

    @staticmethod
    def _fix_sample_video(url: str, tree) -> str:
        return tree.xpath("//div[@id='js-c-box-video']/video")[0].get("src")
