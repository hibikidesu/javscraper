from typing import List, Optional
from datetime import datetime
from urllib.parse import urljoin, urlencode
from .utils import *

import time
import re
from selenium import webdriver

__all__ = ["TenMusume"]


# Site is dynamic and cant be bothered to implement websockets
class TenMusume:

    def __init__(self, english: bool = False, driver=None, headless: bool = True):
        self.english: bool = english

        self.BASE: str = f"https://www.10musume.com"
        if english:
            self.BASE = f"https://en.10musume.com"

        # Create driver
        if driver is None:
            opts = webdriver.FirefoxOptions()
            if headless:
                opts.add_argument("--headless")
            driver = webdriver.Firefox(options=opts)

        self.driver = driver

    def search(self, query: str, **kwargs) -> List[str]:
        """
        Searches for videos with given query.
        :param query: Search terms
        :param kwargs: Extra params to specify
        :return: List of found URLs
        """
        # Make request
        params = urlencode({"s": query, **kwargs})
        self.driver.get(f"{self.BASE}/search/?{params}")

        # Wait for dynamic elements
        time.sleep(3)

        # Get videos
        out = []
        for r in self.driver.find_elements_by_class_name("grid-item"):
            a_tag = r.find_element_by_tag_name("a")
            out.append(urljoin(self.driver.current_url, a_tag.get_attribute("href")))

        return out

    def get_video(self, video: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param video: JAV code or video URL
        :return: JAV results
        """
        # Search for a URL if not given one
        if self.BASE not in video:
            video = f"{self.BASE}/movies/{video}/"

        code = re.search(r"/movies/([0-9_]*)", video).group(1)

        # Perform request
        out = {"studio": "10musume", "code": code}
        self.driver.get(video)

        # If 404
        try:
            self.driver.find_element_by_class_name("fof-image")
            return None
        except:
            pass

        # Wait for site
        time.sleep(3)

        try:
            image = self.driver.find_element_by_id("video-player-0_html5_api")
            out["image"] = urljoin(self.driver.current_url, image.get_attribute("poster"))
        except:
            player_image = self.driver.find_element_by_class_name("player-image")
            out["image"] = urljoin(self.driver.current_url, player_image.find_element_by_tag_name("img").get_attribute("src"))

        title = self.driver.find_element_by_class_name("heading")
        out["name"] = title.find_element_by_tag_name("h1").text

        if not self.english:
            description = self.driver.find_element_by_tag_name("p")
            out["description"] = description.text

        # Common data
        table = self.driver.find_element_by_class_name("movie-info")
        table = table.find_element_by_tag_name("ul")
        for li in table.find_elements_by_tag_name("li"):
            name = li.find_element_by_class_name("spec-title").text
            if name in ["配信日", "Release Date"]:
                value = li.find_element_by_class_name("spec-content")
                out["release_date"] = datetime.strptime(
                    value.text.strip().partition(" ")[0],
                    "%Y/%m/%d"
                )
            elif name in ["出演", "Featuring"]:
                out["actresses"] = []
                for actress in li.find_elements_by_tag_name("a"):
                    out["actresses"].append(actress.text)
            elif name in ["タグ", "Tags"]:
                out["genres"] = []
                for genre in li.find_elements_by_tag_name("a"):
                    out["genres"].append(genre.text)

        return JAVResult(**out)

    def close(self):
        """
        Closes the current driver in use
        :return:
        """
        self.driver.close()
