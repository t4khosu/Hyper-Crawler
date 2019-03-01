import re, requests
from urllib.parse import urlparse

def urlIsValid(url, ignoredExtensions=[]):
    for e in ignoredExtensions:
        if "."+e in url.lower():
            return False
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def isForeignReference(href, crawler):
    if getSecondLevelDomain(href) in crawler.netloc.replace("www.", ""):
        return False
    return True

def getNetloc(url):
    """ Extract netLoc from given URL

    >>> https://www.google.de/...
    >>> www.google.de
    """
    return urlparse(url).netloc

def getSecondLevelDomain(url):
    """ Extract second-level-domain from given URL

    >>> https://www.google.de/...
    >>> google
    """
    return urlparse(url).netloc.replace('www.', '').split('.')[0]

def cleanURL(url):
    """ Clean URLs

    1. check if url is set, if not return empty string
    2. remove '/' at the end of each URL
    """
    if not url:
        return ''
    if url[-1] == '/':
        return url[:-1]
    return url

def cleanForeignUrl(url):
    try:
        return requests.get(url).url
    except:
        return url

def validateAndCleanUrl(url):
    """ Check if each URL is valid and exchange with clean link, if necessary

    Args:
        urls (set) : raw URLS that must be checked
    """
    response = requests.get(url).url
    return response

def validatedURL(url, ignoredExtensions, crawler):
    """ Validation cleans an url and checks if it is valid afterwards """
    url = cleanURL(url)

    if url and url[0] == '/':
        url = crawler.domain + url
    if(urlIsValid(url, ignoredExtensions=ignoredExtensions)):
        return url
    return None