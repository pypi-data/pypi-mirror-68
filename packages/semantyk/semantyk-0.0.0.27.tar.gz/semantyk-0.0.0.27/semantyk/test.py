from core.graph import Graph
from namespace import RDFS, SMTK

r = Graph()
r.add_value(RDFS.isDefinedBy, SMTK)
r.uri = r._generate_uri()
print(r)