import asyncio
import time
from urllib.parse import urlparse

import aiohttp
from aiohttp import client_exceptions
from bs4 import BeautifulSoup
from tqdm import tqdm

from hyper_crawler import settings


class Crawler:
    def __init__(self, *, domain, depth):
        self.domain = domain
        self.depth = depth

        self.netloc = urlparse(domain).netloc
        self.nodes = [domain]
        self.session = None

        self.visited = set()
        self.foreign = []

    async def run(self):
        """Crawl a given domain by collection sub-domains and crawling these, too.

        How many sub-domains get crawled depends on the `self.depth` parameter.
        """

        actual_depth = 0

        while actual_depth < self.depth:
            print(f"Layer: {actual_depth}")
            actual_depth += 1

            layer_responses = await self.__fetch_requests()
            self.__evaluate_responses(layer_responses)

    def __evaluate_responses(self, responses):
        new_nodes = set()

        for url, response in tqdm(responses):
            self_references, foreign_references = self.__evaluate_response(
                url, response
            )
            self.foreign.extend(foreign_references)
            self.visited.add(url)
            new_nodes = new_nodes.union(self_references)

        self.nodes = new_nodes - self.visited

    def __evaluate_response(self, url, response_text):
        foreign_references = []
        self_references = set()

        for href in Crawler.__references_generator(url, response_text):
            if self.__is_foreign_reference(href):
                foreign_references.append(href)
            else:
                self_references.add(href)

        return self_references, foreign_references

    def serialized(self):
        """Create a serialized dict of `self`"""

        return {
            "root": self.domain,
            "depth": self.depth,
            "visited": list(self.visited),
            "foreign": self.foreign,
            "not_visited": list(self.nodes),
        }

    def generate_filename(self):
        return (
                self.netloc.replace(".", "-")
                + "-"
                + time.strftime("%Y%m%d-%H%M%S")
                + ".json"
        )

    def __is_foreign_reference(self, href):
        other_netloc = urlparse(href).netloc
        return other_netloc != self.netloc

    async def __fetch_requests(self):
        async with aiohttp.ClientSession() as session:
            responses = [await self.__fetch(node, session) for node in tqdm(self.nodes)]

        return responses

    @staticmethod
    def __references_generator(url, response_text):
        soup = BeautifulSoup(response_text, "lxml")

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]

            if not href:
                continue

            if href[0] == "/":
                href = url + href

            if href[-1] == "/":
                href = href[:-1]

            if any(
                    "." + extension in href.lower()
                    for extension in settings.IGNORED_EXTENSIONS
            ):
                continue

            if href[:4] != "http":
                continue

            yield href

    @staticmethod
    async def __fetch(url, session):
        try:
            async with session.get(url) as resp:
                response_text = await resp.text()
                await asyncio.sleep(1 / 5)

                return url, response_text
        except client_exceptions.ClientConnectorSSLError as ssl_error:
            print(f"SSL Error {ssl_error}")
        except Exception as e:
            print(f"Unknown Exception occured: {e}")

        return url, ""
