import argparse
import json
import os

import matplotlib.pyplot as plt

from hyper_crawler import settings
from hyper_crawler.crawler import Crawler


async def execute_from_command_line():
    parser = argparse.ArgumentParser(description="Create a reference map for a specific domain")
    subparsers = parser.add_subparsers(dest='parser')

    parser_crawl = subparsers.add_parser('crawl', help='Crawl domain and sub-sites')
    parser_crawl.add_argument("-r", required=True, dest="root", help="root domain")
    parser_crawl.add_argument("-d", dest="depth", default=2, type=int, help="depth of recursion")

    parser_plot = subparsers.add_parser('plot', help='Plot references map')
    parser_plot.add_argument("-i", required=True, dest="input_file", type=str, help='File name in output directory')

    args = parser.parse_args()

    try:
        settings.BASE_DIR
    except ImportError as ie:
        raise ie

    if args.parser == 'crawl':
        await crawl(args)
    elif args.parser == 'plot':
        plot(args)


async def crawl(args):
    crawler = Crawler(domain=args.root, depth=args.depth)
    await crawler.run()

    output_path = os.path.join(settings.OUTPUT_DIR, crawler.generate_filename())

    with open(output_path, "w") as f_out:
        json.dump(crawler.serialized(), f_out)


def plot(args):
    plt.figure(0).canvas.set_window_title(
        title + "[" + str(self.minRefs) + "_bis_" + str(self.maxRefs) + "]"
    )

    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)
