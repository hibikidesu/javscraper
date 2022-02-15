from typing import List, Optional
from urllib.parse import urljoin
from datetime import datetime
from difflib import get_close_matches
from .utils import *

from lxml import html as l_html

__all__ = ["Base"]


class Base:

    def __init__(self, *, base_url: str, debug: bool = False):
        self.PARAMS = {
            "base_url": "https://example.com",
            "cookies": {},
            "headers": {},
            "allow_redirects": False,
            "date_fmt": "",
            "fail_callback": None,
            "encoding": "utf-8",
            "search_xpath": "",
            "video_xpath": {}
        }
        self._set_base_url(base_url)
        self.debug: bool = debug

    # Helper functions

    def _set_base_url(self, base_url: str):
        self.PARAMS["base_url"] = base_url

    def _set_cookies(self, cookies: dict):
        self.PARAMS["cookies"] = cookies

    def _set_headers(self, headers: dict):
        self.PARAMS["headers"] = headers

    def _set_date_fmt(self, fmt: str):
        self.PARAMS["date_fmt"] = fmt

    def _set_fail_callback(self, fail_callback):
        self.PARAMS["fail_callback"] = fail_callback

    def _set_encoding(self, encoding: str):
        self.PARAMS["encoding"] = encoding

    def _set_allow_redirects(self, allow_redirects: bool):
        self.PARAMS["allow_redirects"] = allow_redirects

    def _set_search_xpath(self, search: str):
        self.PARAMS["search_xpath"] = search

    def _set_video_xpath(self, video_xpath: dict):
        self.PARAMS["video_xpath"] = video_xpath

    def _build_search_path(self, query: str) -> str:
        raise NotImplementedError()

    def _build_video_path(self, query: str) -> Optional[str]:
        raise NotImplementedError()

    def _make_normal_search(self, path: str) -> List[str]:
        url = self.PARAMS["base_url"] + path
        if self.debug:
            print(f"URL: {url}")
        with SCRAPER.get(url,
                         allow_redirects=self.PARAMS["allow_redirects"],
                         cookies=self.PARAMS["cookies"],
                         headers=self.PARAMS["headers"]) as res:
            # Check for errors
            try:
                res.raise_for_status()
            except:
                if self.debug:
                    print(f"Failed to make request, {res.status_code}")
                return []

            # Check for redirects
            redirect_location = res.headers.get("Location")
            if redirect_location and not self.PARAMS["allow_redirects"]:
                # Return redirect url if any
                if self.debug:
                    print(f"Redirecting to {redirect_location}")
                return [urljoin(res.url, redirect_location)]

            tree = l_html.fromstring(res.content.decode(self.PARAMS["encoding"], errors="ignore"))

        items = tree.xpath(self.PARAMS["search_xpath"])
        if self.debug:
            print(f"Items: {items}")

        out = [urljoin(res.url, item.get("href")) for item in items]
        if self.debug:
            print(f"Out: {out}")

        return out

    def _make_normal_video(self, url: str) -> Optional[JAVResult]:
        if self.debug:
            print(f"URL: {url}")
        with SCRAPER.get(url,
                         cookies=self.PARAMS["cookies"],
                         headers=self.PARAMS["headers"]) as res:
            # Check for errors
            try:
                res.raise_for_status()
                callback = self.PARAMS["fail_callback"]
                if callable(callback):
                    callback(res)
            except:
                return None

            # Parse data
            tree = l_html.fromstring(res.content.decode(self.PARAMS["encoding"]))

        out = {}
        for name in self.PARAMS["video_xpath"]:
            xpath = self.PARAMS["video_xpath"][name]

            # If is functions
            if callable(xpath):
                out[name] = xpath(res.url, tree)
            else:
                found = tree.xpath(xpath)

                if self.debug:
                    print(name, found)

                if found:
                    if name in ["actresses", "genres"]:
                        out[name] = [x.text_content().strip() for x in found]
                    elif name == "release_date":
                        value = found[0].text_content().strip()
                        out[name] = datetime.strptime(value, self.PARAMS["date_fmt"])
                    else:
                        out[name] = found[0].text_content().strip()

        return JAVResult(**out)

    # Callable functions

    def search(self, query: str, *, code: str = None) -> List[str]:
        """
        Searches for videos with given query.
        :param query: Search terms
        :param code: Code for closest match if not in query
        :return: List of found URLs
        """
        # Build URL
        path = self._build_search_path(query)
        if self.debug:
            print(f"Path: {path}")

        # Make request
        return get_close_matches(code or query, self._make_normal_search(path), cutoff=0)

    def get_video(self, video: str) -> Optional[JAVResult]:
        """
        Returns data for a found jav
        :param video: JAV code or URL
        :return: JAV results
        """
        # Build URL
        if not video.startswith("http"):
            video = self._build_video_path(video)
            if video is None:
                return None

        # Make request
        return self._make_normal_video(video)
