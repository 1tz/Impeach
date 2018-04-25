# coding=utf-8
# v means faster while x means slower
# v     list    x   dict
# v     numpy   x   csv

import os

import numpy as np
from flask import Flask, render_template, send_from_directory

# Define a custom dType: nodeDType
nodeDType = np.dtype(
    [('id', np.str_, 20), ('x', np.float16), ('y', np.float16), ('z', np.float16)])
# Load position of nodes
nodeId, nodeX, nodeY, nodeZ = np.loadtxt('../generateGraph/Weibo/Layout/nodes.csv', dtype=nodeDType, delimiter=',',
                                         unpack=True)
nodeX /= 200
nodeY /= 200
nodeZ /= 200

# 1D arrays -> 2D arrays, then stack them
nodes = np.hstack((nodeId[:, np.newaxis], nodeX[:, np.newaxis], nodeY[:, np.newaxis], nodeZ[:, np.newaxis]))

# Change nDArray to list, which is easier to handle for js
nodesResult = nodes.tolist()

edgeDType = np.dtype([('source', np.str_, 20), ('target', np.str_, 20), ('weight', np.float16)])
edges = np.loadtxt('../generateGraph/Weibo/Layout/edges.csv', dtype=edgeDType, delimiter=',')
edgesResult = edges.tolist()

with open('../generateGraph/Weibo/GraphInfo/info.txt', 'r') as f:
    isWeaklyConnected = f.readline().lower()
    isStronglyConnected = f.readline().lower()
    avgSPL = f.readline()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def view():
    return render_template('index.html', nodes=nodesResult, edges=edgesResult, weak=isWeaklyConnected,
                           strong=isStronglyConnected, avgspl=avgSPL)


# Add an icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='favicon.ico')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
