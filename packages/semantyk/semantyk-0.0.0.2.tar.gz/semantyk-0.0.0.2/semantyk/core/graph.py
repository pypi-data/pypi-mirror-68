##############################################
#
# Graph
# Module | Module Graph.
#
# Daniel Bakas Amuchastegui
# March 16, 2020
# 
# Copyright © Semantyk 2020. All rights reserved.
#############################################

from .node import Node

class Graph(Node):
    _vertices:set

    def _get_nodes(self):
        return self.dictionary
    def _set_nodes(self, nodes:dict):
        self.dictionary = nodes
    nodes = property(_get_nodes, _set_nodes)

    def _get_vertices(self):
        return self._vertices
    def _set_vertices(self, vertices:set):
        self._vertices = vertices
    vertices = property(_get_vertices, _set_vertices)

    def add_nodes(self, *nodes:Node):
        for node in nodes:
            if node.id not in self:
                self.nodes[node.id] = node.dictionary
            
    def delete_nodes(self, *nodes:Node):
        for node in nodes:
            if node.id in self:
                del self.nodes[node.id]

    def __eq__(self, other):
        return super().__eq__(other) and self.vertices == other.vertices

    def __hash__(self):
        return hash(self.id)

    def __init__(self, id:str, nodes:dict = None, vertices:set = None):
        super().__init__(id)
        self.nodes = nodes or dict()
        self.vertices = vertices

    def __iter__(self):
        for node in self.nodes:
            yield node 