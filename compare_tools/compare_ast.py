#!/usr/bin/env python
""" Usage: call with <filename1> <filename2>
"""

from __future__ import unicode_literals
from __future__ import print_function

import sys
import tempfile
import uuid
import clang.cindex


P = 1003


class Ast:
    edges = None
    nodes = None
    gr = None
    hashes = None
    sizes = None
    root = None

    def __init__(self, edges):
        self.edges = edges
        self.gr = {}
        self.hashes = {}
        self.sizes = {}
        self.get_nodes()
        self.create_graph()

    def get_nodes(self):
        if self.nodes:
            return self.nodes
        self.nodes = set()
        for x, y in self.edges:
            if x is None:
                self.root = y
            else:
                self.nodes.add(x)
                self.nodes.add(y)
        return self.nodes

    def create_graph(self):
        for x, y in self.edges:
            if x not in self.gr:
                self.gr[x] = []
            self.gr[x].append(y)

    def hash_dfs(self, cur=None):
        cur = cur or self.root
        hashes = []
        for child in self.gr.get(cur, []):
            hashes.append(self.hash_dfs(child))

        hashes.sort()
        cur_hash = 1
        for h in hashes:
            cur_hash = cur_hash * P + h

        self.hashes[cur] = cur_hash
        return cur_hash

    def size_dfs(self, cur=None):
        cur = cur or self.root
        cur_size = 1
        for child in self.gr.get(cur, []):
            cur_size += self.size_dfs(child)
        self.sizes[cur] = cur_size
        return cur_size

    def get_size(self, v=None):
        v = v or self.root
        if v not in self.sizes:
            return self.size_dfs(v)
        return self.sizes[v]

    def remove_node(self, v):
        self.nodes.remove(v)
        self.root = None if self.root == v else self.root
        for child in self.gr.get(v, [])[:]:
            self.remove_node(child)
        self.gr.pop(v, None)
        for cur in self.gr.keys():
            try:
                self.gr[cur].remove(v)
            except:
                continue

        self.hashes = {}
        self.sizes = {}
        self._used = None


def _create_str(node):
    return "{} {} {}".format(
        str(node.kind).split(".")[1],
        node.spelling or node.displayname, node.spelling)


def create_tree(node, tree_edges, filename, parent=None, level=0):
    this_uuid = str(uuid.uuid4())
    tree_edges.append((parent, this_uuid))
    print("\t" * level + _create_str(node), file=sys.stderr)
    for c in node.get_children():
        if str(c.location.file) != filename:
            continue
        create_tree(c, tree_edges, filename, parent=this_uuid, level=level + 1)


def get_ast(filename):
    index = clang.cindex.Index.create()
    tu = index.parse(filename)
    print('Translation unit:', tu.spelling, file=sys.stderr)

    tree_edges = []

    create_tree(tu.cursor, tree_edges, filename)

    return tree_edges


def find_max_subtree(ast1, ast2):
    ast1.size_dfs()
    ast2.size_dfs()
    ast1.hash_dfs()
    ast2.hash_dfs()

    hashes1 = []
    for v, h in ast1.hashes.items():
        hashes1.append((h, ast1.get_size(v), v))
    hashes2 = []
    for v, h in ast2.hashes.items():
        hashes2.append((h, ast2.get_size(v), v))

    hashes1.sort()
    hashes2.sort()

    max_subtree = (0, None, None)

    for h1, s1, v1 in hashes1:
        for h2, s2, v2 in hashes2:
            if h1 == h2:
                assert s1 == s2
                if s1 > max_subtree[0]:
                    max_subtree = (s1, v1, v2)

    return max_subtree


def tree_similarity(ast1, ast2):
    result = 0.0
    T = 1.0
    print(len(ast1.nodes), len(ast2.nodes), file=sys.stderr)

    founded = []

    while len(ast1.nodes) and len(ast2.nodes):
        res, v1, v2 = find_max_subtree(ast1, ast2)
        print(res, ast1.get_size(), ast2.get_size(), file=sys.stderr)

        founded.append((res, ast1.get_size(), ast2.get_size()))

        result += T * (res * 2.0) / (len(ast1.nodes) + len(ast2.nodes))
        T *= 1 - max(res * 1.0 / len(ast1.nodes), res * 1.0 / len(ast2.nodes))
        print(result, T, file=sys.stderr)
        ast1.remove_node(v1)
        ast2.remove_node(v2)

    return min(1.0, result)


def main():
    if len(sys.argv) != 3:
        print("Usage: {0} source1 source2".format(sys.argv[0]))
        sys.exit(1)

    try:
        temp = tempfile.NamedTemporaryFile(suffix=".cpp")
        temp.write(open(sys.argv[1]).read())
        temp.seek(0)
        ast1 = Ast(get_ast(temp.name))
        temp = tempfile.NamedTemporaryFile(suffix=".cpp")
        temp.write(open(sys.argv[2]).read())
        temp.seek(0)
        ast2 = Ast(get_ast(temp.name))
    except Exception as e:
        print(e, file=sys.stderr)
        print(-1)
        sys.exit(1)

    print(tree_similarity(ast1, ast2))


if __name__ == "__main__":
    main()
