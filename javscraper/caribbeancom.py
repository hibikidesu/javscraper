from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from urllib.parse import urljoin
from .utils import *

import re


class Caribbeancom:

    def __init__(self, language: str = "ja"):
        """
        Creates a caribbeancom instance
        :param language: Result language, either ja, en or cn
        """
        self.language: str = language
        if language == "ja":
            self.BASE = "https://www.caribbeancom.com"
        elif language == "en":
            self.BASE = "https://en.caribbeancom.com/eng"
        elif language == "cn":
            self.BASE = "https://cn.caribbeancom.com"
        else:
            raise ValueError(f"Invalid language, {language}")

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
            f"{self.BASE}/search/",
            params={
                "q": query.encode("euc-jp"),
                **kwargs
            }
        )

        # Check for errors
        result.raise_for_status()

        # Parse videos
        out = []
        soup = BeautifulSoup(result.content, "lxml")

        for div in soup.find_all("div", {"itemtype": "http://schema.org/VideoObject"}):
            out.append(urljoin(result.url, div.find("a")["href"]))

        return out

    def get_video(self, video: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param video: JAV code or URL
        :return: JAV results
        """
        # Search for a URL if not given one
        if self.BASE not in video:
            video = video.lower().replace("_", "-").replace("caribbeancom-", "")
            video = f"{self.BASE}/moviepages/{video}/index.html"

        # Perform request
        result = perform_request("GET", video)

        # Error check
        if result.status_code == 404:
            return None

        result.raise_for_status()

        # Parse contents
        code = re.search(r"moviepages/([0-9-]*)", video).group(1)
        out = {"code": code, "studio": "Caribbeancom"}
        soup = BeautifulSoup(result.content, "lxml")

        # Title
        out["name"] = soup.find("h1", {"itemprop": "name"}).text

        # English videos don't give 404 but instead 200 with no data
        if out["name"] == "":
            return None

        # Description
        out["description"] = soup.find("p", {"itemprop": "description"}).text

        # Image
        out["image"] = f"{self.BASE}/moviepages/{code}/images/l_l.jpg"
        out["sample_video"] = f"https://smovie.caribbeancom.com/sample/movies/{code}/480p.mp4"

        # Parse table
        if self.language == "cn":
            table = soup.find("div", {"itemtype": "http://schema.org/VideoObject"})
            for item in table.find_all("dl"):
                name = item.find("dt").text
                if name == "演员:":
                    out["actresses"] = [x.find("span").text for x in item.find_all("a")]
                elif name == "分类:":
                    out["genres"] = [x.text for x in item.find_all("a")]
                elif name == "发行日期:":
                    value = item.find("dd").text
                    out["release_date"] = datetime.strptime(value, "%Y/%m/%d")
        else:
            table = soup.find("ul", {"itemtype": "http://schema.org/VideoObject"})
            for item in table.find_all("li"):
                name = item.find("span", {"class": "spec-title"}).text
                if name in ["出演", "Starring:"]:
                    out["actresses"] = [x.find("span").text for x in item.find_all("a")]
                elif name in ["タグ", "Tags:"]:
                    out["genres"] = [x.text for x in item.find_all("a")]
                elif name in ["配信日", "Release Date:"]:
                    value = item.find("span", {"class": "spec-content"}).text
                    out["release_date"] = datetime.strptime(value, "%Y/%m/%d")

        return JAVResult(**out)
