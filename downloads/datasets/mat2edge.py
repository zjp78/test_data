#!/usr/bin/env ffi
# encoding: utf-8

import scipy.io
import math


def load_adjacency_matrix(file):
    data = scipy.io.loadmat(file)
    return data['network'], data['group']


def mat2edge(file, edge_output, group_output):
    print("mat2edgelist from %s to %s" % (file, edge_output))
    A, G = load_adjacency_matrix(file)
    A.eliminate_zeros()
    min_v, max_v = min(A.data) , max(A.data)
    print("minimum non-zero value=%.2f maximum non-zero value=%.2f" \
            % (min_v, max_v))
    unweighted = math.isclose(min_v, 1.0) and math.isclose(max_v, 1.0)
    print("unweighted graph" if unweighted else "weighted graph")
    A = A.todok()
    with open(edge_output, "w") as f:
        for (x, y), v in A.items():
            assert(math.isclose(A[y, x], v))
            print("%d\t%d" % (x, y) if unweighted else "%d\t%d\t%f" % (x, y, v), end="\n", file=f)
    with open(group_output, "w") as f:
        for (x, y), v in G.items():
            print("%d\t%d" % (x, y), end="\n", file=f)


if __name__ == "__main__":
    mat2edge("flickr.mat", "flickr.edge", "flickr.group")
    # mat2edge(sys.argv[1], sys.argv[2])
