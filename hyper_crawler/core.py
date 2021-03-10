import argparse
import json
import os
from urllib.parse import urlparse

import matplotlib.pyplot as plt
import networkx as nx

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

    with open(output_path, "w", encoding='utf-8') as f_out:
        json.dump(crawler.serialized(), f_out)


def plot(args):
    input_path = os.path.join(settings.OUTPUT_DIR, args.input_file)

    try:
        with open(input_path, 'r') as file:
            data = json.load(file)
    except OSError as e:
        print(e.errno)
        return

    domain = data['root']
    foreign_references = data['foreign']
    netloc_counts = {}

    for foreign in foreign_references:
        netloc = urlparse(foreign).netloc
        if netloc not in netloc_counts:
            netloc_counts[netloc] = 1
        else:
            netloc_counts[netloc] += 1

    nodes = [0]
    labels = {0: domain}
    sizes = [2]
    edges = []
    edge_labels = {}

    sorted_counts = list(netloc_counts.items())
    sorted_counts.sort(key=lambda x: x[1], reverse=True)

    node = 1
    for (label, size) in sorted_counts[:49]:
        nodes.append(node)
        labels[node] = label
        sizes.append(size)
        edges.append((0, node))
        edge_labels[(0, node)] = size
        node += 1

    print(len(nodes))

    plt.figure(0).canvas.set_window_title(domain)

    plt.gca().set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
    plt.margins(0, 0)

    g = nx.DiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    pos = nx.spring_layout(g, k=0.85, iterations=200)
    nx.draw_networkx_nodes(g, pos, node_size=sizes, alpha=0.4)
    nx.draw_networkx_labels(g, pos, labels, font_weight="normal", font_size=6)
    nx.draw_networkx_edges(g, pos, style="dashed", alpha=0.1, arrows=True)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)

    print("plot")
    plt.show()
