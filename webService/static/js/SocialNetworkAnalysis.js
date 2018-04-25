/**
 *
 * File name:   SocialNetworkAnalysis.js
 * Version:     1.0
 * Date:        2018.3.27
 * Author:      1tz
 * Notes:       This file calculates attributes of
 *              graph
 *
 * only support NON-CIRCULAR DIRECTED GRAPH at present
 * which means it can be changed to a BINARY TREE
 */

// Node
function Node(id, x, y, z) {
    this.id = id;
    this.x = x;
    this.y = y;
    this.z = z;
    this.color = 0;
    this.depth = -1;
    this.inDegree = 0;
    this.outDegree = 0;
    this.pageRank = 0;
    this.children = null;
    this.brother = null;
}

// Edge
function Edge(source, target, weight) {
    this.source = source;
    this.target = target;
    this.weight = weight;
}

// SocialNetworkAnalysis
function SocialNetworkAnalysis(nodeList, edgeList) {
    var nodeListLength = nodeList.length;
    var edgeListLength = edgeList.length;

    // Average Degree
    var avgDegree = edgeListLength / nodeListLength;

    // Average Weighted Degree
    var i, avgWeight, totalWeight = 0;
    for (i = 0; i < edgeListLength; ++i) {
        totalWeight += edgeList[i].weight;
    }
    avgWeight = totalWeight / nodeListLength;

    // Find node by id
    // @return Node / null
    function findNode(id) {
        for (var i = 0; i < nodeListLength; ++i) {
            if (nodeList[i].id === id)
                return nodeList[i];
        }
        return null;
    }

    // Find a tree's root. Perhaps it is useful for other kind of data
    // @return Node
    function findRoot() {
        for (var i = 0; i < nodeListLength; ++i) {
            if (nodeList[i].outDegree !== 0 && nodeList[i].inDegree === 0)
                return nodeList[i];
        }
    }

    // Build a binary tree according to edge list
    // @return null
    function buildTree() {
        var p, pre;
        for (var i = 0; i < edgeListLength; ++i) {
            var sourceNode = findNode(edgeList[i].source);
            var targetNode = findNode(edgeList[i].target);
            if (sourceNode !== null && targetNode !== null) {
                // Calculate degree
                ++targetNode.inDegree;
                ++sourceNode.outDegree;

                // Calculate PageRank
                sourceNode.pageRank += 1.0 / (targetNode.inDegree + targetNode.outDegree);
                targetNode.pageRank += 1.0 / (sourceNode.inDegree + sourceNode.outDegree);

                p = sourceNode.children;
                if (p === null)
                    sourceNode.children = targetNode;
                else {
                    while (p) {
                        pre = p;
                        p = p.brother;
                    }
                    pre.brother = targetNode;
                }
            }
        }
    }

    var depthCount = 0;

    // Calculate diameter
    // @return int
    function calcDiameter() {
        var max = 0, tmp, d = 0.85; // d is a parameter of PageRank
        buildTree();
        for (var i = 0; i < nodeListLength; ++i) {
            tmp = calcDepth(nodeList[i]);
            depthCount += tmp;
            if (tmp > max)
                max = tmp;
            // Calculate PageRank
            nodeList[i].pageRank = d * nodeList[i].pageRank + (1 - d) / nodeListLength;
        }
        return max - 1; // max_depth - 1 = diameter
    }

    // Calculate depth of node
    // @return int
    function calcDepth(node) {
        // A null node will return 0
        if (node === null)
            return 0;
        // Node isn't null and it is not searched
        if (node.depth === -1) {
            // Children's depth
            var sonDepth = calcDepth(node.children);
            // Brother's depth
            var broDepth = calcDepth(node.brother);
            node.depth = Math.max(sonDepth + 1, broDepth);
        }
        return node.depth;
    }

    // Call calcDiameter
    // Ref: https://github.com/gephi/gephi/wiki/Diameter
    var diameter = calcDiameter();

    // Calculate density
    // Ref: https://github.com/gephi/gephi/blob/6efb108718fa67d1055160f3a18b63edb4ca7be2/modules/StatisticsPlugin/src/main/java/org/gephi/statistics/plugin/GraphDensity.java
    var density = edgeListLength / (nodeListLength * nodeListLength - nodeListLength);

    this.avgDegree = avgDegree.toFixed(4);
    this.avgWeight = avgWeight.toFixed(4);
    this.diameter = diameter;
    this.density = density.toFixed(4);
    this.avgShortestPathLength = 0;
    this.isWeaklyConnected = true;
    this.isStronglyConnected = true;
}