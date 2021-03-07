import argparse
import json
import os
import time

from hyper_crawler import settings
from hyper_crawler.crawler import Crawler


async def execute_from_command_line():
    parser = argparse.ArgumentParser(description='Create a reference map for a specific domain')
    parser.add_argument('-r', dest='root', required=True, help='root domain')
    parser.add_argument('-d', dest='depth', default=2, type=int, help='depth of recursion')
    args = parser.parse_args()

    try:
        settings.BASE_DIR
    except ImportError as ie:
        raise ie

    crawler = Crawler(domain=args.root, depth=args.depth)
    await crawler.run()

    file_name = crawler.netloc.replace('.', '-') + '-' + time.strftime("%Y%m%d-%H%M%S") + '.json'
    output_path = os.path.join(settings.OUTPUT_DIR, file_name)

    with open(output_path, 'w') as f_out:
        json.dump(crawler.serialized(), f_out)
