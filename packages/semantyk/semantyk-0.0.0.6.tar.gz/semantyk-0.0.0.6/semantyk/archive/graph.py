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

from .resource import Resource
from ..core import graph
from ..core.node import Node
from ..namespace import RDF, RDFS, SMTK, XSD
from rdflib import Literal, URIRef

class Graph(graph.Graph):
    _triples:set

    def _get_triples(self):
        return self._triples
    def _set_triples(self, triples:set):
        self._triples = triples
    triples = property(_get_triples, _set_triples)

    def _get_objects(self):
        for s,p,o in self.triples:
            yield o
    objects = property(_get_objects)

    def _get_object_predicates(self):
        for s,p,o in self.triples:
            yield (o, p)
    object_predicates = property(_get_object_predicates)

    def _get_object_subjects(self):
        for s,p,o in self.triples:
            yield (o, s)
    object_subjects = property(_get_object_subjects)

    def _get_predicates(self):
        for s,p,o in self.triples:
            yield p
    predicates = property(_get_predicates)

    def _get_predicate_objects(self):
        for s,p,o in self.triples:
            yield (p, o)
    predicate_objects = property(_get_predicate_objects)

    def _get_predicate_subjects(self):
        for s,p,o in self.triples:
            yield (p, s)
    predicate_subjects = property(_get_predicate_subjects)

    def _get_subjects(self):
        for s,p,o in self.triples:
            yield s
    subjects = property(_get_subjects)

    def _get_subject_objects(self):
        for s,p,o in self.triples:
            yield (s, o)
    subject_objects = property(_get_subject_objects)

    def _get_subject_predicates(self):
        for s,p,o in self.triples:
            yield (s, p)
    subject_predicates = property(_get_subject_predicates)

    def _get_linked(self):
        triples = set()
        for s,p,o in self.triples:
            if isinstance(o, URIRef):
                triples.add((s,p,o))
        return Graph(self.id, triples = triples)
    linked = property(_get_linked)

    def _get_quantitative(self, linked:bool = False):
        triples = set()
        for s,p,o in self.triples:
            if (isinstance(o, Literal) and isinstance(o.value, (int, float)) and not isinstance(o.value, bool)):
                triples.add((s,p,o.value))
            if linked and isinstance(o, URIRef):
                triples.add((s,p,o.value))
        return Graph(self.id, triples = triples)
    quantitative = property(_get_quantitative)

    def _get_qualitative(self, linked:bool = False):
        triples = set()
        for s,p,o in self.triples:
            if isinstance(o, Literal) and (not isinstance(o.value, (int, float)) or isinstance(o.value, bool)):
                triples.add((s,p,o.value))
            if linked and isinstance(o, URIRef):
                triples.add((s,p,o.value))
        return Graph(self.id, triples = triples)
    qualitative = property(_get_qualitative)

    def add(self, *triples:tuple):
        for triple in triples:
            self.triples.add(triple)
    
    def remove(self, *triples:tuple):
        for triple in triples:
            self.triples.remove(triple)

    def to_dict(self):
        dictionary = dict()
        for (s,p,o) in self.triples:
            if str(s) not in dictionary:
                dictionary[str(s)] = dict()
            if str(p) not in dictionary[str(s)]:
                dictionary[str(s)][str(p)] = set()
            dictionary[str(s)][str(p)].add(o)
        return dictionary

    def to_resources(self):
        for s in self.to_dict():
            yield Resource(dictionary = self.to_dict()[s], uri = URIRef(s))

    def update(self, new_triple:tuple, old_triple:tuple):
        self.triples.remove(old_triple)
        self.triples.add(new_triple)

    def __init__(self, id:str = None, nodes:dict = None, triples:set = None, vertices = None):
        super().__init__(id, nodes, vertices)
        self.triples = triples

    def __iter__(self):
        for triple in self.triples:
            yield triple

    def __str__(self):
        result = str()
        for resource in self.to_resources():
            result += str(resource)
        return result