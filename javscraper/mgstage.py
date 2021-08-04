from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from .utils import *

__all__ = ["MGStage"]


class MGStage:
    BASE = "https://www.mgstage.com"

    def __init__(self):
        # Age check
        SCRAPER.cookies.set("adc", "1")

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
            f"{self.BASE}/search/cSearch.php",
            params={
                "search_word": query,
                **kwargs
            }
        )

        # Check for errors
        result.raise_for_status()

        # Get videos
        soup = BeautifulSoup(result.content, "lxml")
        data = soup.find("div", {"class": "rank_list"})

        # If missing div
        if data is None:
            return []

        out = []
        for r in data.find_all("li"):
            # Build full URL
            out.append(self.BASE + r.find("a")["href"])

        return out

    def get_video(self, code: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param code: JAV code
        :return: JAV results
        """
        # Perform request
        result = perform_request(
            "GET",
            f"{self.BASE}/product/product_detail/{code}/"
        )
        result.raise_for_status()

        # Get data
        out = {"code": code}
        soup = BeautifulSoup(result.content, "lxml")

        common_data = soup.find("div", {"class": "common_detail_cover"})
        if not common_data:
            return None

        # Get title
        title = common_data.find("h1", {"class": "tag"})
        if title:
            out["name"] = title.text.strip()

        # Get image
        image = common_data.find("a", {"id": "EnlargeImage"})
        if image:
            out["image"] = image["href"]

        # Get common data, changes depending on video
        # Find the table responsible for data
        detail_data = common_data.find("div", {"detail_data"})
        if len(detail_data.find_all("table")) > 1:
            table = detail_data.find_all("table")[1]
        else:
            table = detail_data.find("table")

        for tr in table.find_all("tr"):
            name = tr.find("th").text
            if name == "出演：":
                out["actresses"] = []
                for a in tr.find_all("a"):
                    out["actresses"].append(a.text.strip())
            elif name == "メーカー：":
                maker = tr.find("a")
                out["studio"] = maker.text.strip()
            elif name == "配信開始日：":
                out["release_date"] = datetime.strptime(tr.find("td").text, "%Y/%m/%d")
            elif name == "ジャンル：":
                out["genres"] = []
                for genre in tr.find_all("a"):
                    out["genres"].append(genre.text.strip())

        # Find description
        description = common_data.find("dl", {"id": "introduction"}).find("p")
        if description:
            out["description"] = description.text

        # Find sample video
        sample_button = soup.find("a", {"class": "button_sample"})
        if sample_button:
            # Find PID
            pid = sample_button["href"].rpartition("/")[2]

            # Make request for video
            sample_video_url = perform_request(
                "GET",
                "https://www.mgstage.com/sampleplayer/sampleRespons.php",
                params={
                    "pid": pid
                }
            ).json()

            # Parse out url if exists
            url = sample_video_url.get("url")
            if url:
                url = url.partition(".ism")[0] + ".mp4"
                out["sample_video"] = url

        return JAVResult(**out)
