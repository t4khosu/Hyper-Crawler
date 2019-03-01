import requests, re, sys, os
from tqdm import tqdm
from bs4 import BeautifulSoup, SoupStrainer
from os.path import dirname as dir, join, exists
from util.URL import *
from util.Concat import dictConcat

class Crawler(object):
    def __init__(self, domain, parameters, resultDir):
        self.domain = domain

        self.resultDir = resultDir
        self.logDir = join(resultDir, 'logs/')
        if not exists(self.logDir):
            os.makedirs(self.logDir)

        self.ignoredExtensions = parameters["ignore"]
        self.headers = parameters["headers"]
        self.logger = parameters["logger"]       

        self.netloc = getNetloc(self.domain)
        self.secondLevelDomain = getSecondLevelDomain(self.domain)
        
        self.visited = set([])
        self.selfReferences = set([domain])
        self.foreignReferences = {}
        self.maxDepth = -1

    def crawl(self, maxDepth=2):
        """ Check given URL recursively with given depth

        If depth = 1, only check given URL for hyperlinks.
        If depth = 2, also check found hyperlinks for more hyperlinks.
        And so on...
        If depth = -1, all sites are searched for references
        This stops, once the max depth is reached or all hyperlinks have been visited

        Args:
            maxDepth (int) : max. recursive depth
        """
        self.maxDepth = maxDepth
        depth = 0
        while len(self.visited) != len(self.selfReferences) and (depth <= self.maxDepth or self.maxDepth == -1):
            selfReferences = set([])
            for url in self.selfReferences:
                if url not in self.visited:
                    if self.logger["active"] and len(self.visited) % self.logger["steps"] == 0:
                        print(">>> Stored")
                        self.writeLog(self.logDir)
                    print("Depth {} : {} [Visited: {}, self-references: {}, new self-references: {}, foreign-references: {}]".format(depth, url, len(self.visited), len(self.selfReferences), len(selfReferences), len(self.foreignReferences)))
                    self.visited.add(url)

                    newSelfReferences, newForeignReferences = self.crawlSite(url)
                    selfReferences = selfReferences.union(newSelfReferences)
                    self.foreignReferences = dictConcat(self.foreignReferences, newForeignReferences)
            depth+=1
            self.selfReferences = self.selfReferences.union(selfReferences)
        self.writeLog(self.logDir)
        self.writeOrderedLog("../results/")

    def crawlSite(self, url):
        """ Find all hrefs of a single webpage

        Differentiate between URLs, that reference to this domain
        and URLs, that reference foreign domains
        """
        try:
            foreignReferences = {}
            selfReferences = set([])

            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "lxml")
                for link in soup.find_all('a', href=True):
                    href = validatedURL(link['href'], self.ignoredExtensions, self)
                    if href:
                        if isForeignReference(href, self):
                            if href not in foreignReferences:
                                foreignReferences[href] = set([url])
                            else:
                                foreignReferences[href].add(url)
                        else:
                            selfReferences.add(href)
            return selfReferences, foreignReferences
        except requests.exceptions.MissingSchema as e:
            print(e)
            return set([]), set([])
        except requests.exceptions.ConnectionError as e:
            print(e)
            return set([]), set([])

    def validateForeignURLs(self):
        """ Go through all foreign URLS, run a request and get a clean url.
        Some URLs are kind of random and only represent a domain of the main page.
        These must be excluded from foreign URLs! This is done right here.
        """
        cleanedForeignReferences = set([])
        for ref in tqdm(self.foreignReferences):
            cleanedForeignUrl = cleanForeignUrl(ref)
            if isForeignReference(cleanedForeignUrl, self):
                cleanedForeignReferences.add(cleanedForeignUrl)
        self.foreignReferences = cleanedForeignReferences

    def writeLog(self, dir):
        """ Create a log file with all self-references and foreign-references """
        filename = self.secondLevelDomain + ".log"
        with open(join(dir, filename), 'w') as fOut:
            fOut.write("DOMAIN||" + self.domain + "\n")
            for r in self.foreignReferences:
                fOut.write("FOREIGN||" + r)
                for source in self.foreignReferences[r]:
                    fOut.write('||' + source)
                fOut.write('\n')
            for own in self.visited:
                fOut.write("SELF||" + own + "\n")
    
    def load(self):
        """ Load a log file """
        with open(join(self.logDir, self.secondLevelDomain + ".log"), 'r') as fIn:
            for line in fIn:
                line = line.replace('\n', '')
                if line:
                    splits = line.split('||')
                    if splits[0] == 'SELF':
                        self.selfReferences.add(splits[1])
                    elif splits[0] == 'FOREIGN':
                        self.foreignReferences[splits[1]] = splits[2:]
                    elif splits[0] == 'DOMAIN':
                        self.domain = splits[1]

    def writeOrderedLog(self, dir):
        """ Create a file that contains all links sorted.

        First each individual netloc is extracted.
        Afterwards for each netloc the found urls are stored as list.
        """ 
        mapping = {}
        for ref in self.foreignReferences:
            domain = getNetloc(ref)
            if domain not in mapping:
                mapping[domain] = [ref]
            else:
                mapping[domain].append(ref)

        sorted_mapping = sorted([(k,len(v)) for k,v in mapping.items()], key=lambda x: x[1])
        keys = [t[0] for t in sorted_mapping]
        with open(join(dir, self.secondLevelDomain + ".anl"), 'w') as fOut:
            fOut.write("domain\t{}\n".format(self.domain))
            fOut.write("depth\t{}\n".format(self.maxDepth))
            fOut.write("amount\t{}\n\n".format(len(self.foreignReferences)))
            for key in keys:
                if len(mapping[key]) >= 1:
                    fOut.write("@{}\n".format(key))
                    for link in mapping[key]:
                        fOut.write("*{} [".format(link))
                        fOut.write(', '.join(self.foreignReferences[link]))
                        fOut.write(']\n')
                    fOut.write("\n")