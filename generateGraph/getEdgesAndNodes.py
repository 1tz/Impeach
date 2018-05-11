# coding=utf-8

import numpy as np

choose = 0

if choose:
    dTypeEdge = np.dtype([('source', np.str_, 16), ('target', np.str_, 16)])
    nDEdges = np.loadtxt('Weibo/res/hubei_details.csv', dtype=dTypeEdge, delimiter=',',
                         usecols=(0, 1), skiprows=1 + 2)
    np.savetxt('Weibo/res/edges.csv', X=nDEdges[...], fmt='%s', delimiter=',')
    nDNodes = np.array(list(set(list(nDEdges['mid']))))
    np.savetxt('Weibo/res/nodes.csv', X=nDNodes[...], fmt='%s', delimiter=',')

else:
    nDEdges = np.loadtxt('Twitter/res/higgs-retweet_network.edgelist', dtype=(np.str_, 8), delimiter=' ',
                         usecols=(0, 1))
    nDNodes = np.array(list(set(list(np.ravel(nDEdges)))))
    print(nDNodes.shape)
    np.savetxt('Twitter/res/nodes.csv', X=nDNodes[...], fmt='%s', delimiter=',')
