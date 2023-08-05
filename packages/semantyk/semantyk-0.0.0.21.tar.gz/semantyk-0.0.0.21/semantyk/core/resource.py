##############################################
#
# resource 
# Module | Resource Module.
#
# Author: Daniel Bakas Amuchastegui
# March 18, 2020
# 
# Copyright © Semantyk 2020. All rights reserved.
#############################################

from semantyk.namespace.namespace import RDF, RDFS, SMTK
from rdflib import Namespace, URIRef

class Resource(object):
    _uri:URIRef

    def _get_uri(self):
        return self._uri
    def _set_uri(self, uri:URIRef):
        self._uri = uri
    uri = property(_get_uri, _set_uri)

    def _get_isDefinedBy(self):
        return self.get_values(str(RDFS.isDefinedBy))
    isDefinedBy = property(_get_isDefinedBy)

    def _get_label(self):
        return self.get_values(str(RDFS.label))
    label = property(_get_label)

    def _get_type(self):
        return self.get_values(str(RDF.type))
    type = property(_get_type)

    def _get_properties(self):
        for p in self.dictionary:
            yield p
    properties = property(_get_properties)

    def _get_subClassOf(self):
        return self.get_values(str(RDFS.subClassOf))
    subClassOf = property(_get_subClassOf)

    def _get_values(self):
        return self.get_values()
    values = property(_get_values)

    def add_properties(self, *properties:str):
        for p in properties:
            if p not in self.dictionary:
                self.dictionary[p] = set()

    def add_values(self, p:str, *objects):
        self.add_properties(p)
        for o in objects:
            self.dictionary[p].add(o)

    def delete_properties(self, *properties:str):
        if not properties:
            properties = self.dictionary
        for p in properties:
            if p in self.dictionary:
                del self.dictionary[p]

    def delete_values(self, p:str, *objects):
        for o in objects:
            if p in self.dictionary:
                self.dictionary[p].remove(o)

    def from_triples(self, triples:set):
        dictionary = dict()
        for (s,p,o) in triples:
            if str(p) not in dictionary:
                dictionary[str(p)] = set()
            dictionary[str(p)].add(o)
        return dictionary
            
    def get_values(self, *properties:str):
        if not properties:
            properties = self.dictionary
        for p in properties:
            if p in self.dictionary:
                for o in self.dictionary[p]:
                    yield o

    def to_triples(self):
        triples = set()
        for p in self.dictionary:
            for o in self.dictionary[p]:
                triples.add((self.uri, URIRef(p), o))
        return triples

    def update_property(self, old_p:str, new_p:str):
        self.dictionary[new_p] = self.dictionary[old_p]
        self.delete_properties(old_p)

    def update_values(self, p:str, old_o, *new_objects):
        self.delete_values(p, old_o)
        self.add_values(p, new_objects)

    def _generate_id(self, uri:URIRef = None):
        if uri and self.dictionary and str(RDFS.isDefinedBy) in self.dictionary:
            return str(uri).replace(list(self.dictionary[str(RDFS.isDefinedBy)])[0], '')
        return super()._generate_id()

    def _generate_uri(self, namespace:Namespace = None):
        result = URIRef((str(namespace or SMTK) + self.id or self._generate_id()))
        if self.dictionary and str(RDFS.isDefinedBy) in self.dictionary:
            result = URIRef(str(list(self.get_value(str(RDFS.isDefinedBy)))[0]) + self.id)
        return result

    def __eq__(self, other):
        return super().__eq__(other) and self.uri == other.uri

    def __hash__(self):
        return hash(self.uri)

    def __init__(self, id:str = None, dictionary:dict = None, triples:set = None, uri:URIRef = None):
        self.dictionary = dictionary or self.from_triples(triples)
        self.id = id or self._generate_id(uri)
        self.uri = uri

    def __iter__(self):
        return self.properties

    def __str__(self):
        result = str()
        result += '\n' + self.id + ':'
        for p in self:
            result += '\n - ' + str(p) + ':'
            for o in self.dictionary[p]:
                result += '\n  - ' + str(o)
        return result