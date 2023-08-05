from core.graph import Graph
from rdflib import URIRef, Literal

triples = {
    (URIRef('http://archive.semantyk.com/Daniel'), URIRef('http://archive.semantyk.com/esta_hermoso'), Literal(True, datatype = 'xsd:boolean')),
    (URIRef('http://archive.semantyk.com/Daniel'), URIRef('http://archive.semantyk.com/esta_hermoso'), Literal(False, datatype = 'xsd:boolean')),
    (URIRef('http://archive.semantyk.com/Daniel'), URIRef('http://archive.semantyk.com/esta_cansado'), Literal(False, datatype = 'xsd:boolean')),
    (URIRef('http://archive.semantyk.com/Ana'), URIRef('http://archive.semantyk.com/esta_cansado'), Literal(True, datatype = 'xsd:boolean'))
} 

g = Graph(triples=triples)