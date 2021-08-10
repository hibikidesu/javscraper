from abc import ABC
from typing import Optional

import re
from urllib.parse import quote
from .base import Base

__all__ = ["Caribbeancom"]


class Caribbeancom(Base, ABC):

    def __init__(self, language: str = "ja"):
        """
        Creates a caribbeancom instance
        :param language: Result language, either ja, en or cn
        """
        self.language: str = language
        if language == "ja":
            base = "https://www.caribbeancom.com"
        elif language == "en":
            base = "https://en.caribbeancom.com/eng"
        elif language == "cn":
            base = "https://cn.caribbeancom.com"
        else:
            raise ValueError(f"Invalid language, {language}")

        super().__init__(base_url=base)
        self._set_date_fmt("%Y/%m/%d")
        self._set_fail_callback(self._fail_callback)
        self._set_search_xpath("//div[@id='main']//*[contains(@class, '-title')]/a")
        self._set_video_xpath({
            "name": "//h1[@itemprop='name']",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": "//a[@itemprop='actor']/span",
            "genres": "//a[@itemprop='genre']",
            "release_date": "//*[@itemprop='uploadDate']",
            "description": "//p[@itemprop='description']",
            "sample_video": self._fix_sample_video
        })

        if self.language == "ja":
            self._set_encoding("euc-jp")
        else:
            self._set_encoding("utf-8")

    def _build_search_path(self, query: str) -> str:
        return f"/search/q={quote(query.encode('euc-jp'))}"

    def _build_video_path(self, query: str) -> Optional[str]:
        query = query.lower().replace("_", "-").replace("caribbeancom-", "")
        return f"{self.PARAMS['base_url']}/moviepages/{query}/index.html"

    @staticmethod
    def _fail_callback(result):
        if b"<title>  - Caribbeancom.com</title>\n" in result.content:
            raise ValueError()

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        return re.search(r"moviepages/([0-9-]*)", url).group(1)

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        return "Caribbeancom"

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        code = Caribbeancom._fix_code(url, tree)
        return f"https://www.caribbeancom.com/moviepages/{code}/images/l_l.jpg"

    @staticmethod
    def _fix_sample_video(url: str, tree) -> str:
        code = Caribbeancom._fix_code(url, tree)
        return f"https://smovie.caribbeancom.com/sample/movies/{code}/480p.mp4"
