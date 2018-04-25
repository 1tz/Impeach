# coding=utf-8
"""
Convert .gml files that Gephi generate to .csv file.
Only maintain these nodes' attribute: x/y/z/id
and these edges' attribute: source target
"""

import networkx as nx
import numpy as np

input = '.gml'
outputNodes = '.csv'
outputEdges = '.csv'

G = nx.read_gml(input)

x = []
y = []
z = []
id = []

for n in G.node:
    id.append(n)
    x.append(G.node[n][u'graphics'][u'x'])
    y.append(G.node[n][u'graphics'][u'y'])
    z.append(G.node[n][u'graphics'][u'z'])

nDX = np.array(x)
nDY = np.array(y)
nDZ = np.array(z)
nDID = np.array(id)

nDType = np.dtype([('id', np.str_, 16), ('x', np.float64), ('y', np.float64), ('z', np.float64)])
Data = np.array(nDID[:, np.newaxis], dtype=nDType)

Data['x'] = nDX[:, np.newaxis]
Data['y'] = nDY[:, np.newaxis]
Data['z'] = nDZ[:, np.newaxis]

np.savetxt(outputNodes, fmt='%s', X=Data[:, 0], delimiter=',')

edge = []

for e in G.edges:
    edge.append(e)

np.savetxt(outputEdges, fmt='%s', X=np.array(edge)[...], delimiter=',')
