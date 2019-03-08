import sys, networkx as nx, matplotlib.pyplot as plt, ntpath

class Graph(object):
    def __init__(self):
        """ Graphic representation of nodes and edges """
        self.mapping = {}

        self.nodes = []
        self.node_sizes = []
        self.labels = {}
        self.color_map = []
        self.edges = []
        self.edge_labels = {}

    def load(self, source, minRefs=2, maxRefs=-1):
        """Source can be a folder or a file
        
        All nodes and edges in each selected file are loaded.
        Either all files in a folder are loaded or a single file.
        This function is not recursive! Deeper structures are ignored. 
        """
        domain = ""
        self.minRefs = minRefs
        self.maxRefs = maxRefs
        with open(source, 'r') as fIn:
            actualDomain = ''
            for line in fIn:
                line = line.replace('\n', '')
                if line:
                    splits = line.split('\t')
                    if splits[0] == 'domain':
                        domain = splits[1]
                    if line[0] == '@':
                        actualDomain = line[1:]
                        self.mapping[actualDomain] = []
                    if line[0] == '*':
                        url = line[1:].split('[')[0]
                        self.mapping[actualDomain].append(url)
        newMapping = {}
        for key in self.mapping:
            if len(self.mapping[key]) >= minRefs and (len(self.mapping[key]) <= maxRefs or maxRefs == -1):
                newMapping[key] = self.mapping[key]
        
        nodeDict = {0 : [domain, 100, 0, '#FF0000']}

        for n, key in enumerate(newMapping):
            nodeDict[n+1] = [key, len(newMapping[key])*500, len(newMapping[key]), '#00B2FF']
        for key in nodeDict:
            self.nodes.append(key)
            self.color_map.append(nodeDict[key][3])
            self.labels[key] = nodeDict[key][0]
            self.node_sizes.append(nodeDict[key][1])
            if key != 0:
                edge = (0, key)
                self.edges.append(edge)
                self.edge_labels[edge] = nodeDict[key][2]

    def draw(self, title):
        """ Draw a graph with all nodes and edges """
        plt.figure(0).canvas.set_window_title(title + "[" + str(self.minRefs) + '_bis_' + str(self.maxRefs) + "]")
        plt.gca().set_axis_off()
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
            hspace = 0, wspace = 0)
        plt.margins(0,0)

        g = nx.DiGraph()
        g.add_nodes_from(self.nodes)
        g.add_edges_from(self.edges)

        pos=nx.spring_layout(g, k=0.85,iterations=200)
        print(self.node_sizes)
        nx.draw_networkx_nodes(g, pos, node_size=self.node_sizes, node_color =self.color_map, alpha=0.4)
        nx.draw_networkx_labels(g, pos, self.labels, font_weight="normal", font_size=6)  
        nx.draw_networkx_edges(g, pos, style="dashed", alpha=0.1, arrows=True)  
        nx.draw_networkx_edge_labels(g, pos, edge_labels=self.edge_labels)
        plt.show()