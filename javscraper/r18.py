from typing import List, Optional
from datetime import datetime
from lxml import html as l_html
from .utils import *

import time
import re


__all__ = ["R18"]


class R18:
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

    def search(self, query: str, **kwargs) -> List[str]:
        """
        Searches for videos with given query.
        :param query: Search terms
        :param kwargs: Extra params to specify
        :return: List of found URLs
        """
        # Perform request
        with SCRAPER.get(f"https://www.r18.com/common/search/searchword={query}/") as result:
            result.raise_for_status()
            tree = l_html.fromstring(result.content.decode("utf-8"))

        # Get video URLs
        return [x.get("href") for x in tree.xpath("//li[@class='item-list']/a")]

    def get_video(self, video: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param video: JAV code or video URL
        :return: JAV results
        """
        # Build URL
        if not video.startswith("http"):
            video = self.search(video)
            if not video:
                return None

            video = video[0]

        video = re.search(r"/detail/-/id=([a-zA-Z0-9_]*)", video).group(1)

        # Perform request
        with SCRAPER.get(f"https://www.r18.com/api/v4f/contents/{video}?lang=en&unit=USD") as result:
            try:
                result.raise_for_status()
            except:
                return None

            content = result.json()

        if content.get("status") != "OK":
            return None

        data = content.get("data", {})
        return JAVResult(
            name=self.uncensor_string(data.get("title")),
            code=data.get("dvd_id").upper(),
            studio=data.get("maker", {}).get("name") if data.get("maker", {}) else {},
            image=data.get("images", {}).get("jacket_image", {}).get("large"),
            actresses=[x.get("name") for x in data.get("actresses", [])],
            genres=[self.uncensor_string(x.get("name")) for x in data.get("categories", [])],
            release_date=datetime.strptime(data.get("release_date"), "%Y-%m-%d %H:%M:%S"),
            sample_video=data.get("sample", {}).get("high")
        )

    def uncensor_string(self, text: str) -> str:
        """
        Uncensors a censored string
        :param text: Censored input
        :return: Uncensored output
        """
        for i in self.UNCENSORED:
            text = text.replace(i, self.UNCENSORED[i])
        return text
