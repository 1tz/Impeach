# coding=utf-8
import math

import numpy as np

TIMES = 1000

choose = 0

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
ZEROS = np.zeros((nodesLength, 1), np.float16)
WEIGHT = np.ones((len(nDEdges), 1), np.int8)

if choose:
    DNodes = np.array(nDNodes['mid'][:, np.newaxis], dtype=np.dtype(
        [('mid', np.str_, 16), ('x', np.float16), ('y', np.float16), ('z', np.float16), ('dx', np.float16),
         ('dy', np.float16), ('dz', np.float16)]))
else:
    DNodes = np.array(nDNodes['id'][:, np.newaxis], dtype=np.dtype(
        [('id', np.str_, 16), ('x', np.float16), ('y', np.float16), ('z', np.float16), ('dx', np.float16),
         ('dy', np.float16), ('dz', np.float16)]))

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

Nodes = DNodes.tolist()
Edges = DEdges.tolist()

# THESE PARAMETERS MUST BE FLOAT (ref: Gephi/Gephi wiki)
SPEED_DIVISOR = 800.0
AREA_MULTIPLICATOR = 10000.0
speed = 1.0
area = 10000.0
gravity = 10.0
maxD = math.sqrt(AREA_MULTIPLICATOR * area) / 10
k = math.sqrt(AREA_MULTIPLICATOR * area) / (1 + nodesLength)

for i in range(1, TIMES + 1):
    # Repulsive Force
    for N1 in Nodes:
        for N2 in Nodes:
            if N1 != N2:
                deltaX = N1[0][1] - N2[0][1]
                deltaY = N1[0][2] - N2[0][2]
                deltaZ = N1[0][3] - N2[0][3]
                dist = float(math.sqrt(deltaX ** 2 + deltaY ** 2 + deltaZ ** 2))
                if dist > 0:
                    n = list(N1[0])
                    repulsiveF = k ** 2 / dist
                    n[4] += deltaX / dist * repulsiveF
                    n[5] += deltaY / dist * repulsiveF
                    n[6] += deltaZ / dist * repulsiveF
                    N1[0] = tuple(n)
    # Attractive Force
    for edge in Edges:
        # binary search is faster
        for node in Nodes:
            if node[0][0] == edge[0][0]:
                ns = node
                break
        for node in Nodes:
            if node[0][0] == edge[0][1]:
                nt = node
                break
        deltaX = ns[0][1] - nt[0][1]
        deltaY = ns[0][2] - nt[0][2]
        deltaZ = ns[0][3] - nt[0][3]
        dist = float(math.sqrt(deltaX ** 2 + deltaY ** 2 + deltaZ ** 2))
        attractiveF = dist * dist / k
        if dist > 0:
            s = list(ns[0])
            t = list(nt[0])
            s[4] -= deltaX / dist * attractiveF
            s[5] -= deltaY / dist * attractiveF
            s[6] -= deltaZ / dist * attractiveF
            s[4] += deltaX / dist * attractiveF
            s[5] += deltaY / dist * attractiveF
            s[6] += deltaZ / dist * attractiveF
            ns[0] = tuple(s)
            nt[0] = tuple(t)
    # Gravity Force
    for node in Nodes:
        d = float(math.sqrt(node[0][1] ** 2 + node[0][2] ** 2 + node[0][3] ** 2))
        gravityF = 0.01 * k * gravity * d
        x = node[0][1]
        y = node[0][2]
        z = node[0][3]
        if d != 0:
            n = list(node[0])
            n[4] -= gravityF * x / d
            n[5] -= gravityF * y / d
            n[6] -= gravityF * z / d
            node[0] = tuple(n)
    for node in Nodes:
        n = list(node[0])
        n[4] *= speed / SPEED_DIVISOR
        n[5] *= speed / SPEED_DIVISOR
        n[6] *= speed / SPEED_DIVISOR
        node[0] = tuple(n)
    for node in Nodes:
        deltaX = node[0][4]
        deltaY = node[0][5]
        deltaZ = node[0][6]
        dist = float(math.sqrt(deltaX ** 2 + deltaY ** 2 + deltaZ ** 2))
        if dist > 0:
            n = list(node[0])
            lDist = min(maxD * (float(speed / SPEED_DIVISOR)), dist)
            n[1] += deltaX / dist * lDist
            n[2] += deltaY / dist * lDist
            n[3] += deltaZ / dist * lDist
            node[0] = tuple(n)
    for node in Nodes:
        n = list(node[0])
        n[4] = 0.0
        n[5] = 0.0
        n[6] = 0.0
        node[0] = tuple(n)
    print(Nodes[0][0][1:4])

nDNodes = np.array(Nodes).reshape(nodesLength, 7)
nDEdges = np.array(Edges).reshape(edgesLength, 3)

if choose:
    np.savetxt('Weibo/Layout/nodes.csv', X=nDNodes[:, 0:4], fmt='%s', delimiter=',')
    np.savetxt('Weibo/Layout/edges.csv', X=nDEdges[...], fmt='%s', delimiter=',')
else:
    np.savetxt('Twitter/Layout/nodes.csv', X=nDNodes[:, 0:4], fmt='%s', delimiter=',')
    np.savetxt('Twitter/Layout/edges.csv', X=nDEdges[...], fmt='%s', delimiter=',')
