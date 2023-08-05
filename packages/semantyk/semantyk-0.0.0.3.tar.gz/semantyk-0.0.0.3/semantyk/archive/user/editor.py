##############################################
#
# editor
# Module | Editor Module.
#
# Daniel Bakas Amuchastegui
# March 18, 2020
# 
# Copyright © Semantyk 2020. All rights reserved.
#############################################

from .user import User
from rdflib import URIRef

class Editor(User): 
    def __init__(self, id:str = None, dictionary:dict = None, triples:set = None, uri:URIRef = None):
        super().__init__(id, dictionary, triples, uri)