from collections import namedtuple



Edge = namedtuple('Edge', ['v1', 'v2', 'dir1', 'dir2']) #dirs are letter, where to go from verticle to edge

class Graph:
    def __init__(self, unordered_edges = True):
        self.unord = unordered_edges
        self.vert_ctr = 0 #next key for verticle
        self.verts = {} #num: coord
        self.edge_ctr = 0 #next key for edge
        self.edges = {} #num: Edge

    def add_vert(self, value):
        if value in self.verts.values(): return
        self.verts[self.vert_ctr] = value
        self.vert_ctr += 1

    def add_edge(self, v1, v2, dir1, dir2):
        if self.unord:
            if v2 < v1: v1,v2=v2,v1; dir1,dir2 = dir2,dir1
        e = Edge(v1, v2, dir1, dir2)
        if e in self.edges.values(): return
        if not v1 in self.verts or not v2 in self.verts:
            raise ValueError('One of verticles ({}, {}) is not in a graph'.format(v1, v2))
        self.edges[self.edge_ctr] = e
        self.edge_ctr += 1

    def add_edge_by_values(self, v1_val, v2_val, dir1, dir2):
        v1 = self.find_vert(v1_val)
        v2 = self.find_vert(v2_val)
        self.add_edge(v1, v2, dir1, dir2)

    def del_edge(self, n):
        self.edges.pop(n)

    def del_vert(self, n):
        for i in self.edges.keys():
            if n in (self.edges[i].v1, self.edges[i].v2):
                self.del_edge(i)

    def find_vert(self, value):
        for i in self.verts.keys():
            if self.verts[i] == value:
                return i
        return None

    def find_edges(self, v1, v2):
        res = []
        for i in self.edges.keys():
            if self.edges[i].v1 == v1 and self.edges[i].v2 == v2:
                res.append(i)
        return res

    def find_edges_by_values(self, v1_val, v2_val):
        res = []
        v1 = self.find_vert(v1_val)
        v2 = self.find_vert(v2_val)
        return res if (v1 == None or v2 == None) else self.find_edges(v1, v2)

    def find_edge(self, v1, v2, dir1, dir2):
        for i in self.edges.keys():
            if self.edges[i] == Edge(v1, v2, dir1, dir2):
                return i
        return None

    def find_edge_by_values(self, v1_val, v2_val, dir1, dir2):
        res = []
        v1 = self.find_vert(v1_val)
        v2 = self.find_vert(v2_val)
        return res if (v1 == None or v2 == None) else self.find_edge(v1, v2, dir1, dir2)

