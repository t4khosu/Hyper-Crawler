import time
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3 import Retry

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

    def start_session(self, *, connect, backoff_factor):
        self.session = requests.Session()
        adapter = HTTPAdapter(max_retries=Retry(connect=connect, backoff_factor=backoff_factor))
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def run(self):
        actual_depth = 0

        while actual_depth < self.depth:
            print(f"Layer: {actual_depth}")
            self.check_and_update_nodes()
            actual_depth += 1

    def check_and_update_nodes(self):
        new_nodes = set()

        for node in tqdm(self.nodes):
            self_references, foreign_references = self.crawl(node)
            self.visited.add(node)

            self.foreign.extend(foreign_references)
            new_nodes = new_nodes.union(self_references)

        self.nodes = new_nodes - self.visited

    def crawl(self, url):
        """Crawl a single URL and collect all references

        Args:
            url (:obj:`str`)

        Returns:
            tuple of a set and list: The set contains all self references and the list all references
                to other domains
        """

        foreign_references = []
        self_references = set()

        response = self.session.get(url=url, headers=settings.REQUEST_HEADERS)
        time.sleep(1.5)

        if not response.status_code == 200:
            return self_references, foreign_references

        for href in Crawler.__references_generator(response):
            if self.__is_foreign_reference(href):
                foreign_references.append(href)
            else:
                self_references.add(href)

        return self_references, foreign_references

    def serialized(self):
        result = {'root': self.domain, 'depth': self.depth, 'visited': list(self.visited), 'foreign': self.foreign}

        return result

    def __is_foreign_reference(self, href):
        other_netloc = urlparse(href).netloc
        return other_netloc != self.netloc

    @staticmethod
    def __references_generator(response):
        soup = BeautifulSoup(response.text, "lxml")

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']

            if not href:
                continue

            if href[0] == '/':
                href = response.url + href[1:]

            if href[-1] == '/':
                href = href[:-1]

            if href[:4] != 'http':
                continue

            yield href
