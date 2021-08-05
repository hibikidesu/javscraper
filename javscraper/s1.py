from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from .utils import *

__all__ = ["S1"]


class S1:
    BASE = "https://s1s1s1.com"

    def search(self, query: str, **kwargs) -> List[str]:
        raise NotImplementedError()

    def get_video(self, code: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param code: JAV code for S1 videos
        :return: JAV results
        """
        # Fix code
        code = code.replace("-", "").strip()

        # Perform request
        result = perform_request(
            "GET",
            f"{self.BASE}/works/detail/{code}"
        )
        result.raise_for_status()

        # Get data
        out = {"studio": "S1 NO.1 STYLE"}
        soup = BeautifulSoup(result.content, "lxml")

        if soup.find("div", {"class": "p-notFound"}):
            return None

        # Get title
        title = soup.find("h2", {"class": "p-workPage__title"})
        if title:
            out["name"] = title.text.strip()

        # Get description
        description = soup.find("p", {"class": "p-workPage__text"})
        if description:
            out["description"] = description.text.strip()

        # Get image
        image = soup.find("img", {"class": "pc"})
        if image:
            out["image"] = image["src"]

        # Get sample video
        sample_video = soup.find("video")
        if sample_video:
            out["sample_video"] = sample_video["src"]

        # Parse table
        table = soup.find("div", {"class": "p-workPage__table"})
        for item in table.find_all("div", {"class": "item"}):
            name = item.find("div", {"class": "th"})
            if name is None:
                continue
            name = name.text
            if name == "女優":
                out["actresses"] = []
                for actress in item.find_all("a"):
                    out["actresses"].append(actress.text)
            elif name == "発売日":
                date = item.find("a").text
                out["release_date"] = datetime.strptime(date, "%Y年%m月%d日")
            elif name == "ジャンル":
                out["genres"] = []
                for genre in item.find_all("a"):
                    out["genres"].append(genre.text)
            elif name == "品番":
                out["code"] = item.find("p").contents[1]

        return JAVResult(**out)
