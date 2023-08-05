##############################################
#
# user 
# Module | User Module.
#
# Author: Daniel Bakas Amuchastegui
# March 18, 2020
# 
# Copyright © Semantyk 2020. All rights reserved.
#############################################

from semantyk.core.resource import Resource
from rdflib import URIRef

class User(Resource):
    def __init__(self, id:str = None, dictionary:dict = None, triples:set = None, uri:URIRef = None):
        super().__init__(id, dictionary, triples, uri)