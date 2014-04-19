# -*- coding: utf-8 -*-

import os.path
import codecs

# Constants

# Node type
CHARACTER   = 1
GROUP       = 2

# Relation type
COMPOSED_OF = 3
VARIANT_OF  = 4

# These codes are used in the file to represent the abovementioned constants.
_constant_codes = {

    'c' : COMPOSED_OF,
    'v' : VARIANT_OF,

    'z' : CHARACTER,  # 'z' for 'zi'; i.e. Mandarin for character
    'g' : GROUP
}

def record_id(record):
    return record[0]

def record_type(record):
    return record[1]

def record_relation_type(record):
    return record[2]

def record_referent(record):
    return record[3]

class Decomposer:

    def __init__(self, file_name):
        self._decomp_table = {}
        self._file_name = file_name
        self._load_decomposition_data()


    # Returns a 4-tuple representing the relation between a node ID
    # and a referent.
    #   1. The node ID. If the node ID has length one, it is considered to represent
    #       a character.  Otherwise, it is a group ID.
    #   2. The node type: (CHARACTER, GROUP)
    #   3. The relation type: (VARIANT_OF, COMPOSED_OF)
    #   4. The referent in the relation.  Either a single character when the
    #           relation is VARIANT_OF or a list of component characters when the
    #           relation is COMPOSED_OF.
    def _parse_line(self, line_string):
        split_line = line_string.strip().split(':')

        # Extract the four fields as strings
        node_id = split_line[0]
        type_string = split_line[1]
        relation_string = split_line[2]
        referent_string = split_line[3]

        # Turn the strings into binary

        # 1. The node type
        node_type = _constant_codes[type_string]

        # 2. The node ID does not need to be parsed

        # 3. The type of relation the node represents
        relation_type = _constant_codes[relation_string]

        # 4. The referent

        # First case, this character is a variant of a primary
        # character. There should only be one character.
        # The referent in this relation is the primary character.
        if relation_type == VARIANT_OF:
            assert(node_type == CHARACTER and len(referent_string) == 1)
            referent = referent_string
        else:
            # Second case, this character is composed of other
            # simpler characters. The referent in this relation
            # is a list of the component characters.
            #
            # The simplest characters have no component characters.
            referent = None
            if len(referent_string) > 0:
                referent = referent_string.split(',')

        return (node_id, node_type, relation_type, referent)

    def _load_decomposition_data(self):
        if not os.path.exists(self._file_name):
            msg = "Decomposition data file does not exist: " + self._file_name
            raise RuntimeError(msg)

        with codecs.open(self._file_name, 'r', encoding='utf-8') as f:
            for line in f:
                record = self._parse_line(line)
                assert(not record_id(record) in self._decomp_table)
                self._decomp_table[record_id(record)] = record

    # Returns a tree. Symbolic references between nodes are resolved
    # into direct references so forming a recursive data structure.
    def decompose(self, ch):
        try:
            record = self._decomp_table[ch]
        except KeyError:
            raise RuntimeError('No decomposition data for ' + repr(ch))

        relation_type = record_relation_type(record)
        if relation_type == COMPOSED_OF:
            component_ids = record_referent(record)
            if component_ids == None: 
                return record
            else:
                # Replace component IDs with references to nodes.
                return (
                    record_id(record),
                    record_type(record),
                    record_relation_type(record),
                    [self.decompose(i) for i in component_ids]
                )
        else:
            assert(relation_type == VARIANT_OF)
            # Replace ID of primary character with a reference to a node.
            return (
                record_id(record),
                record_type(record),
                record_relation_type(record),
                self.decompose(record_referent(record))
            )

    def __str__(self):
        return str(self._decomp_table)

def is_unicode_kangxi_radical(ch):
    # See http://en.wikipedia.org/wiki/Kangxi_Radicals#Unicode
    return u'⼀' <= ch and ch <= u'⿕'

def is_unicode_supplemental_radical(ch):
    # See ttp://en.wikipedia.org/wiki/CJK_Radicals_Supplement
    return u'⺀' <= ch and ch <= u'⻳' 

def is_unicode_radical(ch):
    return is_unicode_kangxi_radical(ch) or is_unicode_supplemental_radical(ch)

def is_unicode_stroke(ch):
    return u'㇀' <= ch and ch <= u'㇣'
