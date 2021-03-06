import argparse

from hyper_crawler import settings
from hyper_crawler.crawler import Crawler


def execute_from_command_line():
    parser = argparse.ArgumentParser(description='Create a reference map for a specific domain')
    parser.add_argument('-d', dest='depth', default=2, type=int, help='depth of recursion')
    parser.add_argument('-r', dest='root', required=True, help='root domain')
    args = parser.parse_args()

    try:
        settings.BASE_DIR
    except ImportError as ie:
        raise ie

    crawler = Crawler(domain=args.root, depth=args.depth)
    crawler.start_session(connect=3, backoff_factor=0.5)
    crawler.run()

    serialized = crawler.serialized()
    print(serialized)
