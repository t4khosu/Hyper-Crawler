import asyncio
from urllib.parse import urlparse

import aiohttp
from bs4 import BeautifulSoup
from tqdm import tqdm


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
        actual_depth = 0

        while actual_depth < self.depth:
            print(f"Layer: {actual_depth}")
            actual_depth += 1

            layer_responses = await self.__fetch_requests()
            self.__evaluate_responses(layer_responses)

    def __evaluate_responses(self, responses):
        new_nodes = set()

        for url, response in responses:
            self_references, foreign_references = self.__evaluate_response(url, response)
            self.foreign.extend(foreign_references)
            new_nodes = new_nodes.union(self_references)

        self.nodes = new_nodes - self.visited

    def __evaluate_response(self, url, response_text):
        """Crawl a single URL and collect all references

        Args:
            url (:obj:`str`)

        Returns:
            tuple of a set and list: The set contains all self references and the list all references
                to other domains
        """

        foreign_references = []
        self_references = set()

        for href in Crawler.__references_generator(url, response_text):
            if self.__is_foreign_reference(href):
                foreign_references.append(href)
            else:
                self_references.add(href)

        return self_references, foreign_references

    def serialized(self):
        return {
            'root': self.domain, 'depth': self.depth, 'visited': list(self.visited),
            'foreign': self.foreign, 'not_visited': list(self.nodes)
        }

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

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']

            if not href:
                continue

            if href[0] == '/':
                href = url + href

            if href[-1] == '/':
                href = href[:-1]

            if href[:4] != 'http':
                continue

            yield href

    @staticmethod
    async def __fetch(url, session):
        async with session.get(url) as resp:
            response_text = await resp.text()
            await asyncio.sleep(1 / 5)

            return url, response_text
