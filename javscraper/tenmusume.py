from typing import List, Optional
from datetime import datetime
from .utils import *

import re

__all__ = ["TenMusume"]


# Site is dynamic and cant be bothered to implement websockets
class TenMusume:

    def __init__(self, english: bool = False):
        self.english: bool = english

    def search(self, query: str) -> List[str]:
        """
        Searches for videos with given query.
        :param query: Search terms
        :return: List of found URLs
        """
        raise NotImplementedError()

    def get_video(self, video: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param video: JAV code or URL
        :return: JAV results
        """
        # Build URL
        if video.startswith("http"):
            video = re.search(r"/movies/([0-9_]*)", video).group(1)
        else:
            video = video.lower().replace("10musume-", "")

        with SCRAPER.get(f"https://en.10musume.com/dyn/phpauto/movie_details/movie_id/{video}.json") as result:
            try:
                result.raise_for_status()
            except:
                return None

            content = result.json()

        out = {}
        out["name"] = content.get("TitleEn") if self.english else content.get("Title")
        out["code"] = content.get("MovieID")
        out["studio"] = "10musume"
        out["image"] = content.get("ThumbUltra")
        out["genres"] = content.get("UCNAMEEn") if self.english else content.get("UCNAME")
        out["release_date"] = datetime.strptime(content.get("Release"), "%Y-%m-%d")
        out["sample_video"] = content.get("SampleFiles", [])[-1:][0].get("url")
        out["description"] = content.get("DescEn") if self.english else content.get("Desc")

        out["actresses"] = []
        for actress in content.get("ActressesList", {}):
            actress_data = content.get("ActressesList", {}).get(actress, {})
            out["actresses"].append(
                actress_data.get("NameEn") if self.english else actress_data.get("NameJa")
            )

        return JAVResult(**out)
