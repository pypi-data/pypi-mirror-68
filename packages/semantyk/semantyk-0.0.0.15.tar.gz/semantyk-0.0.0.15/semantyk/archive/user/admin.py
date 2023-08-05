##############################################
#
# admin
# Module | Admin Module.
#
# Daniel Bakas Amuchastegui
# March 18, 2020
# 
# Copyright © Semantyk 2020. All rights reserved.
#############################################

from semantyk.archive.user import User
from rdflib import URIRef

class Admin(User): 
    def __init__(self, id:str = None, dictionary:dict = None, triples:set = None, uri:URIRef = None):
        super().__init__(id, dictionary, triples, uri)