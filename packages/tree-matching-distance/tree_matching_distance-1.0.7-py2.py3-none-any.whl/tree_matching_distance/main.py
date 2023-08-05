import argparse
import sys
from tree_matching_distance import __version__

import networkx as nx
from ete3 import Tree


def distance(t1, t2):
    '''
    Compute and return the distance proposed by Lin et al (2011), also known
    as tree matching distance.

    Input: two trees from ETE3.
    Returns: an integer
    '''

    if len(t1.get_leaves()) < 4 or len(t2.get_leaves()) < 4:
        raise ValueError('Need at least 4 leaves in input trees.')

    rf, max_rf, common_leaves, parts_t1, parts_t2, *more = t1.robinson_foulds(t2, unrooted_trees=True)
    # We are actually only interested in the last two parameters

    G = nx.Graph()
    partitions1 = list(map(_setify, filter(_non_trivial_partition, parts_t1)))
    partitions2 = list(map(_setify, filter(_non_trivial_partition, parts_t2)))

    start_for_p2 = len(partitions1)
    for vertex_id1, p1 in enumerate(partitions1):
        for vertex_id2, p2 in enumerate(partitions2, start_for_p2):
            w = _compute_weight(p1, p2)
            G.add_edge(vertex_id1, vertex_id2, weight=w)

    matching = nx.bipartite.minimum_weight_full_matching(G)

    matching_weight = 0
    for v1 in matching:
        v2 = matching[v1]
        weight = G.get_edge_data(v1, v2)['weight']
        matching_weight += weight

    # Every edge in the matching is picked up twice, because of the way the
    # matching is represented, so we return half the sum to not bias distance upward.
    return matching_weight // 2


def _non_trivial_partition(p):
    '''
    Return True iff partition p is non-trivial, i.e., both parts contains at least two elements.
    '''
    a, b = p
    return len(a) > 1 and len(b) > 1


def _setify(p):
    a, b = p
    return set(a), set(b)

def _compute_weight(partition1, partition2):
    '''
    The weight is the difference in elements of the partitions.
        p1 = abc|de     => 11100
        p2 = ac|cde     => 10100
        D(p1, p2) = min(Hamming(11100, 10100), Hamming(11100,01011)) = min(1, 4)=1

        p1 = adefg|bch  => 10011110
        p2 = abcfg|deh  => 11100110
        D = min(Hamming(10011110, 11100110), Hamming(10011110, 00011001)) = min(4,4)=4
        or
        d = min(symdiff(adefg,abcfg), symdiff(adefg,deh)) = min(4,4)=4
    '''

    diff1 = len(partition1[0].symmetric_difference(partition2[0]))
    diff2 = len(partition1[0].symmetric_difference(partition2[1]))
    return min(diff1, diff2)



def main(argv):
    ap = argparse.ArgumentParser(description='Compute tree distance using a metric by Lin et al.')
    ap.add_argument('--version', action='version', version=f'tree_matching_distance {__version__}')
    ap.add_argument('treefile1', help='A file containing a tree on Newick format')
    ap.add_argument('treefile2', help='A file containing a tree on Newick format')
    args = ap.parse_args(argv)

    try:
        t1 = Tree(args.treefile1)
    except Exception as e:
        ap.exit(f'Error reading tree in file {args.treefile1}')
    try:
        t2 = Tree(args.treefile2)
    except Exception as e:
        ap.exit(f'Error reading tree in file {args.treefile2}')

    try:
        d = distance(t1, t2)
        print(d)
    except Exception as e:
        print('Error computing tree matching distance.', file=sys.stderr)
        print(e, file=sys.stderr)
        ap.exit(1)

def run():
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
