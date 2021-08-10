from abc import ABC
from typing import Optional

import re
from urllib.parse import quote
from .base import Base
from .utils import perform_request

__all__ = ["MGStage"]


class MGStage(Base, ABC):

    def __init__(self):
        super().__init__(base_url="https://www.mgstage.com")
        self._set_cookies({"adc": "1"})
        self._set_date_fmt("%Y/%m/%d")
        self._set_fail_callback(self._fail_callback)
        self._set_search_xpath("//div[@class='rank_list']/ul/li/h5/a")
        self._set_video_xpath({
            "name": "//div[@class='common_detail_cover']/h1",
            "code": self._fix_code,
            "studio": "//tr[th='メーカー：']/td/a",
            "image": self._fix_image,
            "actresses": "//tr[th='出演：']/td/a",
            "genres": "//tr[th='ジャンル：']/td/a",
            "release_date": "//tr[th='配信開始日：']/td",
            "description": "//p[contains(@class, 'introduction')]",
            "sample_video": self._fix_sample_video
        })

    def _build_search_path(self, query: str) -> str:
        return f"/search/cSearch.php?search_word={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        return f"{self.PARAMS['base_url']}/product/product_detail/{query}/"

    @staticmethod
    def _fail_callback(result):
        if result.url == "https://www.mgstage.com/":
            raise ValueError()

    @staticmethod
    def _fix_code(url: str, tree) -> str:
        return re.search(r"product_detail/([a-zA-Z0-9-_]*)", url).group(1)

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        return tree.xpath("//a[@id='EnlargeImage']")[0].get("href")

    @staticmethod
    def _fix_sample_video(url: str, tree):
        sample_button = tree.xpath("//a[@class='button_sample']")[0].get("href")
        if sample_button:
            # Find PID
            pid = sample_button.rpartition("/")[2]

            # Make request for video
            sample_video_url = perform_request(
                "GET",
                "https://www.mgstage.com/sampleplayer/sampleRespons.php",
                params={
                    "pid": pid
                },
                cookies={"adc": "1"}
            ).json()

            # Parse out url if exists
            url = sample_video_url.get("url")
            if url:
                url = url.partition(".ism")[0] + ".mp4"
                return url
        return None
