from bs4 import BeautifulSoup
from typing import List, Optional
from datetime import datetime
from .utils import *

import time
import re
from selenium import webdriver


__all__ = ["R18"]


class R18:
    BASE = "https://www.r18.com"

    def __init__(self, driver=None, headless: bool = True):
        """
        Creates a scraper for R18 using a given driver
        :param driver: Selenium driver, if none is given, Firefox (geckodriver) will be used
        """
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
        # Perform request
        result = perform_request(
            "GET",
            f"{self.BASE}/common/search/searchword={query}/"
        )
        result.raise_for_status()

        # Get video URLs
        out = []
        soup = BeautifulSoup(result.content, "lxml")

        for i in soup.find_all("li", {"class": "item-list"}):
            out.append(i.find("a")["href"])

        return out

    def get_video(self, video: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param video: JAV code or video URL
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
        out = {}
        self.driver.get(video)

        # Sleep for cloudflare?
        time.sleep(6)

        # Get title
        title = self.driver.find_element_by_class_name("sc-dTSxUT")
        out["name"] = title.text

        # Parse common data
        # 1st div of data
        for i in self.driver.find_elements_by_class_name("iYqFvi"):
            name = i.find_element_by_tag_name("h3").text
            if name == "Actresses":
                out["actresses"] = []
                for actress in i.find_elements_by_tag_name("a"):
                    out["actresses"].append(actress.text)
            elif name == "Categories":
                out["genres"] = []
                for genre in i.find_elements_by_tag_name("a"):
                    out["genres"].append(genre.text)
            elif name == "Studio":
                out["studio"] = i.find_element_by_tag_name("a").text

        # 2nd div of data
        dmm_url = None
        for i in self.driver.find_elements_by_class_name("cBOAnd"):
            name = i.find_element_by_tag_name("h3").text
            if name == "Content ID":
                video_path = "videoc" if "/amateur/" in video else "videoa"
                content_id = i.find_element_by_tag_name("div").text
                dmm_url = f"https://www.dmm.co.jp/digital/{video_path}/-/detail/=/cid={content_id}/"
            elif name == "Release date":
                release_date = i.find_element_by_tag_name("div").text
                out["release_date"] = datetime.strptime(release_date, "%b %d, %Y")
            elif name == "DVD ID":
                out["code"] = i.find_element_by_tag_name("div").text

        # Get description from DMM since r18 does not provide descriptions
        if dmm_url:
            result = perform_request("GET", dmm_url, cookies={"age_check_done": "1"})
            soup = BeautifulSoup(result.content, "lxml")
            out["description"] = soup.find_all("div", {"class": "mg-b20"})[1].text.strip()

        # Get sample video
        sample_iframe = self.driver.find_element_by_class_name("sc-dPaNSN")

        # Make request for iframe data
        self.driver.get(sample_iframe.get_attribute("src"))
        time.sleep(1)

        # Get video src
        video_tag = self.driver.find_element_by_tag_name("video")
        video = video_tag.find_elements_by_tag_name("source")[-1:][0]
        out["sample_video"] = video.get_attribute("src")

        # Get image
        image = self.driver.find_element_by_class_name("vjs-poster")
        match = re.match(r"background-image: url\(\"(.+)\"\);", image.get_attribute("style"))
        out["image"] = match.group(1)

        return JAVResult(**out)
