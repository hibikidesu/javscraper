from typing import List, Optional
from datetime import datetime
from urllib.parse import urljoin
from .utils import *

import time
import requests
from selenium import webdriver

__all__ = ["SOD"]


class SOD:
    BASE = "https://ec.sod.co.jp"

    def __init__(self, driver=None, headless: bool = True):
        """
        Creates a scraper for SOD using a given driver
        :param driver: Selenium driver, if none is given, Firefox (geckodriver) will be used
        :param headless: Run the default driver in headless mode
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
        self.make_request(
            f"{self.BASE}/prime/videos/genre/?search_type=1&sodsearch={query}"
        )

        out = []
        videos = self.driver.find_elements_by_class_name("videis_s_txt")

        for video in videos:
            a_tag = video.find_element_by_tag_name("a")
            out.append(urljoin(self.driver.current_url, a_tag.get_attribute("href")))

        return out

    def get_video(self, code: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param code: JAV code for SOD videos
        :return: JAV results
        """
        # Perform request
        out = {}
        self.make_request(
            f"{self.BASE}/prime/videos/?id={code}"
        )

        if code not in self.driver.current_url:
            return None

        # Get the title from the last h1 found
        title = self.driver.find_elements_by_tag_name("h1")[-1:][0]
        out["name"] = title.text

        # Get the description
        description = self.driver.find_element_by_tag_name("article")
        out["description"] = description.text

        # Get the image
        self.driver.find_element_by_class_name("popup-image").click()
        time.sleep(0.1)
        out["image"] = self.driver.find_element_by_class_name("mfp-img").get_attribute("src")
        self.driver.find_element_by_class_name("mfp-close").click()

        # Parse common
        table = self.driver.find_element_by_tag_name("table")
        for item in table.find_elements_by_tag_name("tr"):
            name = item.find_element_by_class_name("v_intr_ti").text
            if name == "品番":
                value = item.find_element_by_class_name("v_intr_tx")
                out["code"] = value.text
            elif name == "発売年月日":
                value = item.find_element_by_class_name("v_intr_tx")
                out["release_date"] = datetime.strptime(value.text, "%Y年 %m月 %d日")
            elif name == "出演者":
                out["actresses"] = []
                for actress in item.find_elements_by_tag_name("a"):
                    out["actresses"].append(actress.text)
            elif name == "メーカー":
                value = item.find_element_by_class_name("v_intr_tx")
                out["studio"] = value.text
            elif name == "ジャンル":
                out["genres"] = []
                for genre in item.find_elements_by_tag_name("a"):
                    out["genres"].append(genre.text)

        return JAVResult(**out)

    def make_request(self, url: str):
        """
        Makes a request, bypassing cloudflare checks if any and age checks
        :param url: URL to get
        :return:
        """
        # Make the request
        self.driver.get(url)

        # Check for cloudflare
        start_time = time.time()
        while self.driver.title.startswith("Just a moment"):
            time.sleep(1)
            if (time.time() - start_time) > 10:
                raise ConnectionError("Unable to get past cloudflare checks.")

        # Check for age check
        try:
            self.driver.find_element_by_class_name("enter").click()
        except:
            pass

    def close(self):
        """
        Closes the current driver in use
        :return:
        """
        self.driver.quit()

    @staticmethod
    def download_image(url: str) -> requests.Response:
        """
        Downloads an image which will normally 403 without referrer header
        :param url: URL to download from cloudfront
        :return: HTTP Response
        """
        return requests.get(url, headers={"Referer": "https://ec.sod.co.jp/"})
