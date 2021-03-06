from urllib.parse import urlparse


def second_level_domain(*, url):
    """ Extract second-level-domain from given URL

    Args:
        url (:obj:`str`)

    Examples:
        >>> second_level_domain(url="https://www.google.de/some/stuff")
        'google'
    """

    return urlparse(url).netloc.replace('www.', '').split('.')[0]
