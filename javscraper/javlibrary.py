from abc import ABC
from typing import Optional

from urllib.parse import quote, urljoin
from .base import Base

__all__ = ["JAVLibrary"]


class JAVLibrary(Base, ABC):

    def __init__(self, region: str = "en"):
        super().__init__(base_url="http://www.javlibrary.com")
        self.region: str = region

        self._set_cookies({"over18": "18"})
        self._set_date_fmt("%Y-%m-%d")
        self._set_search_xpath("/html/body/div[3]/div[2]/div[2]/div/div[@class='video']/a")
        self._set_video_xpath({
            "name": self._fix_name,
            "code": "//div[@id='video_id']/table/tr/td[2]",
            "studio": "//div[@id='video_maker']/table/tr/td[2]/span/a",
            "image": self._fix_image,
            "actresses": "//span[@class='star']/a",
            "genres": "//span[@class='genre']/a",
            "release_date": "//div[@id='video_date']/table/tr/td[2]"
        })

    def _build_search_path(self, query: str) -> str:
        return f"/{self.region}/vl_searchbyid.php?keyword={quote(query)}"

    def _build_video_path(self, query: str) -> Optional[str]:
        video_url = self.search(query)
        if len(video_url) == 0:
            return None
        return video_url[0]

    @staticmethod
    def _fix_image(url: str, tree) -> str:
        value = tree.xpath("//img[@id='video_jacket_img']")[0]
        return urljoin(url, value.get("src"))

    @staticmethod
    def _fix_name(url: str, tree) -> str:
        value = tree.xpath("//h3[contains(@class, 'post-title')]")[0].text_content()
        code = tree.xpath("//div[@id='video_id']/table/tr/td[2]")[0].text_content()
        return value.replace(code, "").strip()
