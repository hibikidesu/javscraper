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
    UNCENSORED = {
        "[Recommended For Smartphones] ": "",
        "A*****t": "Assault",
        "A*****ted": "Assaulted",
        "A****p": "Asleep",
        "A***e": "Abuse",
        "B***d": "Blood",
        "B**d": "Bled",
        "C***d": "Child",
        "D******ed": "Destroyed",
        "D******eful": "Shameful",
        "D***k": "Drunk",
        "D***king": "Drinking",
        "D**g": "Drug",
        "D**gged": "Drugged",
        "F***": "Fuck",
        "F*****g": "Forcing",
        "F***e": "Force",
        "G*********d": "Gang Banged",
        "G*******g": "Gang bang",
        "G******g": "Gangbang",
        "H*********n": "Humiliation",
        "H*******ed": "Hypnotized",
        "H*******m": "Hypnotism",
        "I****t": "Incest",
        "I****tuous": "Incestuous",
        "K****p": "Kidnap",
        "K**l": "Kill",
        "K**ler": "Killer",
        "K*d": "Kid",
        "Ko**ji": "Komyo-ji",
        "Lo**ta": "Lolita",
        "M******r": "Molester",
        "M****t": "Molest",
        "M****ted": "Molested",
        "M****ter": "Molester",
        "M****ting": "Molesting",
        "P****h": "Punish",
        "P****hment": "Punishment",
        "P*A": "PTA",
        "R****g": "Raping",
        "R**e": "Rape",
        "R**ed": "Raped",
        "S*********l": "School Girl",
        "S*********ls": "School Girls",
        "S********l": "Schoolgirl",
        "S********n": "Submission",
        "S******g": "Sleeping",
        "S*****t": "Student",
        "S***e": "Slave",
        "S***p": "Sleep",
        "S**t": "Shit",
        "Sch**l": "School",
        "Sch**lgirl": "Schoolgirl",
        "Sch**lgirls": "Schoolgirls",
        "SK**lful": "Skillful",
        "SK**ls": "Skills",
        "StepB****************r": "Stepbrother and Sister",
        "StepM************n": "Stepmother and Son",
        "StumB**d": "Stumbled",
        "T*****e": "Torture",
        "U*********sly": "Unconsciously",
        "U**verse": "Universe",
        "V*****e": "Violate",
        "V*****ed": "Violated",
        "V*****es": "Violates",
        "V*****t": "Violent",
        "Y********l": "Young Girl",
        "R*pe": "Rape",
        "D******e": "Disgrace",
    }

    def __init__(self, driver=None, headless: bool = True):
        """
        Creates a scraper for R18 using a given driver
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

        # Cloudflare checks
        start_time = time.time()
        while self.driver.title.startswith("Just a moment"):
            time.sleep(1)
            if (time.time() - start_time) > 10:
                raise ConnectionError("Unable to get past cloudflare checks.")

        # Get title
        title = self.driver.find_element_by_class_name("sc-dTSxUT")
        out["name"] = self.uncensor_string(title.text)

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
                    out["genres"].append(self.uncensor_string(genre.text))
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

    def uncensor_string(self, text: str) -> str:
        """
        Uncensors a censored string
        :param text: Censored input
        :return: Uncensored output
        """
        for i in self.UNCENSORED:
            text = text.replace(i, self.UNCENSORED[i])
        return text

    def close(self):
        """
        Closes the current driver in use
        :return:
        """
        self.driver.close()
