import json, sys, argparse
from components.Crawler import Crawler
# from components.Graph import Graph
from util.URL import *
from os.path import join



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extrahiere referenzierte Webseiten bezüglich einer Seite.')
    parser.add_argument('-d', dest='depth', default=2, type=int, help='Rekursionstiefe, bezüglich der gegebenen Seite.')
    parser.add_argument('-l', dest='link', default='', help='Wurzel und Hauptseite, von der aus rekursiv verlinkungen gesucht werden.')
    parser.add_argument('-p', dest='p', action='store_true', help='Arbeite eine Liste von Seiten ab, die in parameters.json gegeben ist.')
    parser.add_argument('-r', dest='recreate', action='store_true', help='Falls bereits eine log-Datei existiert, erstelle lediglich die .anl-Datei')
    args = parser.parse_args()

    with open("parameters.json") as fIn:
	    parameters = json.load(fIn)

    ignoredExtensions = parameters["ignore"]
    resultDir = '../results/'

    if args.p:
        sites = parameters["sites"]
        for site in sites:
            c = Crawler(site, parameters, resultDir)
            c.crawl(maxDepth=args.depth)
    elif args.link:
        c = Crawler(args.link, parameters, resultDir)
        if args.recreate:
            c.load()
            c.writeOrderedLog(resultDir)
        else:
            c.crawl(maxDepth=args.depth)
    else:
        print("Es wurde keine passende Webseite angegeben...")