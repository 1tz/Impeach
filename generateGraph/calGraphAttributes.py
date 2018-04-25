# coding=utf-8

import networkx as nx
import numpy as np

dTypeEdge = np.dtype([('last_mid', np.str_, 16), ('mid', np.str_, 16)])
dTypeNode = np.dtype([('mid', np.str_, 16)])
nDNodes = np.loadtxt('Weibo/res/nodes.csv', dtype=dTypeNode, unpack=True)['mid']
nDEdges = np.loadtxt('Weibo/res/edges.csv', dtype=dTypeEdge, delimiter=',')

G = nx.DiGraph()
G.add_nodes_from(nDNodes)
G.add_edges_from(nDEdges)

with open('Weibo/GraphInfo/info.txt', 'wb') as f:
    w = str(nx.is_weakly_connected(G))
    s = str(nx.is_strongly_connected(G))
    avgSPL = str(nx.average_shortest_path_length(G))
    f.write(w + '\n' + s + '\n' + avgSPL)

