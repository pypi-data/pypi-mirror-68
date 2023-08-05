##############################################
#
# Node
# Module | Module Node.
#
# Daniel Bakas Amuchastegui
# March 16, 2020
# 
# Copyright © Semantyk 2020. All rights reserved.
#############################################

import uuid

class Node(object):
    _dictionary:dict
    _id:str

    def _get_dictionary(self):
        return self._dictionary
    def _set_dictionary(self, dictionary:dict):
        self._dictionary = dictionary
    dictionary = property(_get_dictionary, _set_dictionary) 

    def _get_id(self):
        return self._id
    def _set_id(self, id:str):
        self._id = id
    id = property(_get_id, _set_id) 

    def _generate_id(self):
        result = '0'
        while result[0] not in {'a', 'b', 'c', 'd', 'e', 'f'}:
            result = uuid.uuid4().hex
            result = result[0:8] + '_' + result[8:12] + '_' + result[12:16] + '_' + result[16:20] + '_' + result[20:]
        return result

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.id == other.id and self.dictionary == other.dictionary

    def __hash__(self):
        return hash(self.id)

    def __init__(self, id:str = None, dictionary:dict = None):
        super().__init__()
        self.id = id or self._generate_id()
        self.dictionary = dictionary or dict()

    def __iter__(self):
        for key in self.dictionary:
            yield key