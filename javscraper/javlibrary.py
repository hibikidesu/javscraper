from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from urllib.parse import urljoin
from .utils import *

__all__ = ["JAVLibrary"]


class JAVLibrary:
    BASE = "http://www.javlibrary.com"

    def __init__(self, region: str = "en"):
        self.region: str = region
        SCRAPER.cookies.set("over18", "18")

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
            f"{self.BASE}/{self.region}/vl_searchbyid.php",
            params={
                "keyword": query,
                **kwargs
            },
            allow_redirects=False
        )

        # Check for errors
        result.raise_for_status()

        # Check if a single video has been found - being redirected to that video
        redirect_location = result.headers.get("Location")
        if redirect_location:
            # Return the URL of the location
            return [urljoin(result.url, redirect_location)]

        soup = BeautifulSoup(result.content, "lxml")

        # Return multiple videos found
        out = []

        videos = soup.find("div", {"class": "videos"})
        for video in videos.find_all("div", {"class": "video"}):
            out.append(urljoin(result.url, video.find("a")["href"]))

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
        result.raise_for_status()

        out = {}
        soup = BeautifulSoup(result.content, "lxml")

        # Find the title
        title = soup.find("h3", {"class": "post-title text"})
        if title:
            out["name"] = title.find("a").text

        # Find the image
        image = soup.find("img", {"id": "video_jacket_img"})
        if image:
            out["image"] = "https:" + image["src"] if not image["src"].startswith("http") else image["src"]

        # Generic video info table
        video_info = soup.find("div", {"id": "video_info"})
        for info in video_info.find_all("div", {"class": "item"}):
            name = info["id"]
            if name == "video_id":
                out["code"] = info.find_all("td")[1].text
            elif name == "video_maker":
                out["studio"] = info.find("a").text
            elif name == "video_date":
                val = info.find_all("td")[1].text
                out["release_date"] = datetime.strptime(val, "%Y-%m-%d")
            elif name == "video_cast":
                actors = info.find("td", {"class": "text"}).find_all("a")
                out["actresses"] = []
                for actor in actors:
                    out["actresses"].append(actor.text)
            elif name == "video_genres":
                genres = info.find("td", {"class": "text"}).find_all("span")
                out["genres"] = []
                for genre in genres:
                    out["genres"].append(genre.find("a").text)

        # Remove code from name if exists
        out["name"] = out["name"].replace(out["code"], "").strip()

        return JAVResult(**out)
