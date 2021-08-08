from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from urllib.parse import urljoin
from .utils import *

import re

__all__ = ["IdeaPocket"]


class IdeaPocket:
    BASE = "https://www.ideapocket.com"

    def search(self, query: str, **kwargs) -> List[str]:
        """
        Searches for videos with given query.
        :param query: Search terms
        :param kwargs: Extra params to specify
        :return: List of found URLs
        """
        # Make request
        result = perform_request(
            "GET",
            f"{self.BASE}/search/list/",
            params={
                "q": query,
                **kwargs
            }
        )

        # Check if nothing found
        if result.status_code == 404:
            return []

        # Check for errors
        result.raise_for_status()

        # Parse videos
        soup = BeautifulSoup(result.content, "lxml")
        out = [
            urljoin(result.url, a["href"])
            for a in soup.find_all("a", {"class": "works-list-item-info"})
        ]

        return out

    def get_video(self, video: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param video: JAV code or URL
        :return: JAV results
        """
        # Search for a URL if not given one
        if self.BASE not in video:
            video_url = self.search(video)
            if len(video_url) == 0:
                # Nothing found
                return None

            # Get first result
            video = video_url[0]

        # Perform request
        result = perform_request("GET", video)

        # Error check
        if result.status_code == 404:
            return None

        result.raise_for_status()

        # Parse contents
        code = re.search(r"/detail/([a-zA-Z0-9_]*)", video).group(1)
        out = {"code": fix_jav_code(code), "studio": "IdeaPocket"}
        soup = BeautifulSoup(result.content, "lxml")

        # Title
        out["name"] = soup.find("div", {"class": "works-info-ttl"}).find("h1").text

        # Description
        out["description"] = soup.find("div", {"class": "works-info-comment"}).find("p").text

        # Image
        out["image"] = f"{self.BASE}/contents/works/{code}/{code}-pl.jpg"

        # Sample video
        sample_div = soup.find("div", {"id": "js-c-box-video"})
        if sample_div:
            out["sample_video"] = sample_div.find("video")["src"]

        # Parse table
        table = soup.find("ul", {"class": "works-info-data-lst"})
        for li in table.find_all("li", {"class": "works-info-data-item"}):
            name = li.find("dt").text
            if name == "女優":
                out["actresses"] = [actress.text for actress in li.find_all("a")]
            elif name == "発売日":
                value = li.find("a").text
                out["release_date"] = datetime.strptime(value, "%Y年%m月%d日")
            elif name == "ジャンル":
                out["genres"] = [genre.text for genre in li.find_all("a")]

        return JAVResult(**out)
