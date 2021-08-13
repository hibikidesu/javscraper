from abc import ABC
from typing import Optional, List

import re
from lxml import html as l_html
from urllib.parse import quote, urljoin
from .base import Base
from .utils import fix_jav_code, jav_code_to_content, SCRAPER

__all__ = ["DMM"]


class DMM(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.dmm.co.jp")
        self._set_date_fmt("%Y/%m/%d")
        self._set_cookies({"age_check_done": "1"})
        self._set_search_xpath("//ul[@id='list']/li/div/p/a[contains(@href, '/video') or contains(@href, '/dvd')]")
        self._set_video_xpath({
            "name": "//div[@class='hreview']/h1",
            "code": self._fix_code,
            "studio": self._fix_studio,
            "image": self._fix_image,
            "actresses": self._fix_actresses,
            "genres": "//table[@class='mg-b20']/tr[contains(td[1], 'ジャンル')]/td[2]//a",
            "release_date": "//table[@class='mg-b20']/tr[contains(td[1], '日')]/td[2]",
            "description": "//div[@class='mg-b20 lh4']",
            "sample_video": self._fix_sample_video
        })

    def _build_search_path(self, query: str) -> str:
        path = f"/search/=/searchstr={quote(query)}"
        return path

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        code = tree.xpath("//table[@class='mg-b20']/tr[contains(td[1], '品番')]/td[2]")[0]
        return fix_jav_code(code.text_content())

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        img = tree.xpath("//a[@name='package-image']")
        if img:
            return img[0].get("href")
        return tree.xpath("//img[@class='tdmm']")[0].get("src")

    @staticmethod
    def _fix_actresses(url: str, tree) -> list:
        actresses = tree.xpath("//table[@class='mg-b20']/tr[contains(td[1], '出演者')]/td[2]//a")
        return [x.text_content() for x in actresses] if actresses else []

    @staticmethod
    def _fix_studio(url: str, tree) -> str:
        studio = tree.xpath("//table[@class='mg-b20']/tr[contains(td[1], 'メーカー')]/td[2]/a")
        if studio:
            return studio[0].text_content()
        return tree.xpath("//table[@class='mg-b20']/tr[contains(td[1], 'レーベル')]/td[2]/a")[0].text_content()

    @staticmethod
    def _fix_sample_video(url: str, tree) -> Optional[str]:
        video = tree.xpath("//a[@class='d-btn']")
        if not video:
            return None
        vid_url = re.search(r"sampleplay\(\'(.+)\'\)", video[0].get("onclick")).group(1)
        vid_url = urljoin(url, vid_url)
        with SCRAPER.get(vid_url) as r:
            try:
                r.raise_for_status()
            except:
                return None
            data = l_html.fromstring(r.content)
        return data.xpath("//iframe")[0].get("src")

    def search(self, query: str) -> List[str]:
        """
        Searches for videos with given query.
        :param query: Search terms
        :return: List of found URLs
        """
        # First pass
        path_1 = self._build_search_path(query)
        out_1 = self._make_normal_search(path_1)

        if len(out_1) > 0:
            return out_1

        # Try again with fixed code
        query = jav_code_to_content(query)
        path_2 = self._build_search_path(query)
        return self._make_normal_search(path_2)
