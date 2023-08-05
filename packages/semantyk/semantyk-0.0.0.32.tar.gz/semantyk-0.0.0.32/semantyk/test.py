from core.graph import Graph
from namespace import RDFS, SMTK

r = Graph(triples={(SMTK.subject, SMTK.predicate, SMTK.object)})
print(list(r.to_resources())[0])