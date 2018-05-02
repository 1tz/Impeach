# coding=utf-8

import math

import numpy as np

TIMES = 1000

choose = 1

if choose:
    dTypeEdge = np.dtype([('last_mid', np.str_, 16), ('mid', np.str_, 16)])
    nDEdges = np.loadtxt('Weibo/res/edges.csv', dtype=dTypeEdge, delimiter=',')
    dTypeNode = np.dtype([('mid', np.str_, 16)])
    nDNodes = np.loadtxt('Weibo/res/nodes.csv', dtype=dTypeNode, unpack=True)

else:
    dTypeEdge = np.dtype([('source', np.str_, 16), ('target', np.str_, 16), ('weight', np.int8)])
    nDEdges = np.loadtxt('Twitter/res/higgs-retweet_network.edgelist', dtype=dTypeEdge, delimiter=' ')

    dTypeNode = np.dtype([('id', np.str_, 8)])
    nDNodes = np.loadtxt('Twitter/res/nodes.csv', dtype=dTypeNode, unpack=True)

nodesLength = len(nDNodes)
edgesLength = len(nDEdges)
X = np.random.rand(nodesLength, 1) * 4 - 2
Y = np.random.rand(nodesLength, 1) * 4 - 2
Z = np.random.rand(nodesLength, 1) * 4 - 2
ZEROS = np.zeros((nodesLength, 1), np.float32)
WEIGHT = np.ones((len(nDEdges), 1), np.int8)

if choose:
    DNodes = np.array(nDNodes['mid'][:, np.newaxis], dtype=np.dtype(
        [('mid', np.str_, 16), ('x', np.float32), ('y', np.float32), ('z', np.float32), ('dx', np.float32),
         ('dy', np.float32), ('dz', np.float32)]))
else:
    DNodes = np.array(nDNodes['id'][:, np.newaxis], dtype=np.dtype(
        [('id', np.str_, 16), ('x', np.float32), ('y', np.float32), ('z', np.float32), ('dx', np.float32),
         ('dy', np.float32), ('dz', np.float32)]))

DNodes['x'] = X
DNodes['y'] = Y
DNodes['z'] = Z
DNodes['dx'] = ZEROS
DNodes['dy'] = ZEROS
DNodes['dz'] = ZEROS

if choose:
    DEdges = np.array(nDEdges['last_mid'][:, np.newaxis],
                      dtype=np.dtype([('last_mid', np.str_, 16), ('mid', np.str_, 16), ('weight', np.int8)]))
    DEdges['mid'] = nDEdges['mid'][:, np.newaxis]
    DEdges['weight'] = WEIGHT

else:
    DEdges = np.array(nDEdges['source'][:, np.newaxis],
                      dtype=np.dtype([('source', np.str_, 16), ('target', np.str_, 16), ('weight', np.int8)]))
    DEdges['target'] = nDEdges['target'][:, np.newaxis]
    DEdges['weight'] = nDEdges['weight'][:, np.newaxis]

SPEED_DIVISOR = 800.0
AREA_MULTIPLICATOR = 10000.0
speed = 1.0
area = 10000.0
gravity = 10.0
maxD = math.sqrt(AREA_MULTIPLICATOR * area) / 10
k = math.sqrt(AREA_MULTIPLICATOR * area) / (1 + nodesLength)

for N1 in DNodes:
    deltaX = DNodes['x'] - N1['x']
    deltaY = DNodes['y'] - N1['y']
    deltaZ = DNodes['z'] - N1['z']
    dist = np.sqrt(deltaX ** 2 + deltaY ** 2 + deltaZ ** 2)
    k2 = k ** 2
    repulsiveF = np.divide(k2, dist, out=np.zeros_like(dist), where=dist != 0)
    N1['dx'] += np.sum(np.divide(deltaX * repulsiveF, dist, out=np.zeros_like(dist), where=dist != 0))


# if choose:
#     np.savetxt('Weibo/Layout/nodes.csv', X=nDNodes[:, 0:4], fmt='%s', delimiter=',')
#     np.savetxt('Weibo/Layout/edges.csv', X=nDEdges[...], fmt='%s', delimiter=',')
# else:
#     np.savetxt('Twitter/Layout/nodes.csv', X=nDNodes[:, 0:4], fmt='%s', delimiter=',')
#     np.savetxt('Twitter/Layout/edges.csv', X=nDEdges[...], fmt='%s', delimiter=',')
