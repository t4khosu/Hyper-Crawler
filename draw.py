import ntpath
import sys
from os.path import join, isfile

from components.Graph import Graph

if __name__ == "__main__":
    parser.add_argument("-f", dest="file", default="", help="Dateiname mit Endung .anl")
    parser.add_argument(
        "--max",
        dest="max",
        type=int,
        default=-1,
        help="Maximale Knotengröße, die vorkommen darf. Für alle Größen, nutze -1",
    )
    parser.add_argument(
        "--min",
        dest="min",
        type=int,
        default=2,
        choices=range(1, 99999999),
        help="Minimale Knotengröße, die vorkommen darf.",
    )
    args = parser.parse_args()

    anlFile = join(args.dir, args.file)
    if not isfile(anlFile):
        print("Die angegebene Datei wurde nicht gefunden...")
        sys.exit(0)
    if args.min > args.max and args.max != -1:
        print("Min muss kleiner als Max sein!")
        sys.exit(0)

    graph = Graph()
    graph.load(anlFile, minRefs=args.min, maxRefs=args.max)
    graph.draw(ntpath.basename(anlFile).split(".")[0])
