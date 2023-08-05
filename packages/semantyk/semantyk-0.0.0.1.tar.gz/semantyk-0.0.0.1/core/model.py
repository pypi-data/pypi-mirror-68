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

from .node import Node

class Model(Node):
    def __init__(self, id = None, dictionary = None):
        super().__init__(id, dictionary)
