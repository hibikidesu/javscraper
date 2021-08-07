from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from urllib.parse import urljoin
from .utils import *

import requests

__all__ = ["SOD"]


class SOD:
    BASE = "https://ec.sod.co.jp"

    def search(self, query: str, **kwargs) -> List[str]:
        """
        Searches for videos with given query.
        :param query: Search terms
        :param kwargs: Extra params to specify
        :return: List of found URLs
        """
        # Perform request
        result = self.make_request(
            f"{self.BASE}/prime/videos/genre/?search_type=1&sodsearch={query}"
        )
        result.raise_for_status()

        # Parse data
        out = []
        soup = BeautifulSoup(result.content, "lxml")

        videos = soup.find_all("div", {"class": "videis_s_txt"})
        for video in videos:
            out.append(urljoin(result.url, video.find("a")["href"]))

        return out

    def get_video(self, code: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param code: JAV code for SOD videos
        :return: JAV results
        """
        # Perform request
        result = self.make_request(
            f"{self.BASE}/prime/videos/?id={code}"
        )
        result.raise_for_status()

        if code not in result.url:
            return None

        out = {}
        soup = BeautifulSoup(result.content, "lxml")

        # Get the title from the last h1 found
        title = soup.find_all("h1")
        if title:
            out["name"] = title[-1:][0].text.strip()

        # Get the description
        description = soup.find("article")
        if description:
            out["description"] = description.text.strip()

        # Parse common
        table = soup.find("table")
        for item in table.find_all("tr"):
            name = item.find("td", {"class": "v_intr_ti"}).text
            if name == "品番":
                value = item.find("td", {"class": "v_intr_tx"})
                out["code"] = value.text
            elif name == "発売年月日":
                value = item.find("td", {"class": "v_intr_tx"})
                out["release_date"] = datetime.strptime(value.text, "%Y年 %m月 %d日")
            elif name == "出演者":
                out["actresses"] = []
                for actress in item.find_all("a"):
                    out["actresses"].append(actress.text)
            elif name == "メーカー":
                value = item.find("td", {"class": "v_intr_tx"})
                out["studio"] = value.text
            elif name == "ジャンル":
                out["genres"] = []
                for genre in item.find_all("a"):
                    out["genres"].append(genre.text)

        # Get the image
        out["image"] = soup.find("div", {"class": "videos_samimg"}).find("a")["href"]

        return JAVResult(**out)

    @staticmethod
    def make_request(url: str) -> requests.Response:
        """
        Makes a request to bypass the age check redirect
        :param url: Url to request
        :return:
        """
        return perform_request(
            "GET",
            "https://ec.sod.co.jp/prime/_ontime.php",
            headers={"Referer": url}
        )

    @staticmethod
    def download_image(url: str) -> requests.Response:
        """
        Downloads an image which will normally 403 without referrer header
        :param url: URL to download from cloudfront
        :return: HTTP Response
        """
        return requests.get(url, headers={"Referer": "https://ec.sod.co.jp/"})
