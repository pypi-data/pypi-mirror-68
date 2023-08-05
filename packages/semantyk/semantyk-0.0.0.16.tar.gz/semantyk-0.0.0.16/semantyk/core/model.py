##############################################
#
# Model
# Module | Module Model.
#
# Daniel Bakas Amuchastegui
# March 20, 2020
# 
# Copyright © Semantyk 2020. All rights reserved.
#############################################

from core.graph import Graph

class Model(Graph):
    def __init__(self, id:str, triples:set = None):
        super().__init__(id, triples = triples)
