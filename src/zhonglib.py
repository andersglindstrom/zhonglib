# -*- coding: utf-8 -*-

import os.path
import codecs

# Enumerations

CHARACTER  = 1
GROUP      = 2

_node_type_map = {
    'z':CHARACTER,  # Use 'z' here rather than 'c' to avoid confusion with COMPOSED_OF
    'g':GROUP
}

COMPOSED_OF = 3
VARIANT_OF  = 4

_relation_map = {
    'c' : COMPOSED_OF,
    'v' : VARIANT_OF
}

class Decomposer:

    def __init__(self, file_name):
        self._decomp_table = {}
        self._file_name = file_name
        self._load_decomposition_data()


    # Returns a 4-tuple representing the relation between a node ID
    # and a referent.
    #   1. The node ID. Either a Unicode character or an integer group ID. To avoid
    #           clashes, group IDs are put into the private use area of the Unicode
    #           code space.  However, they do not represent actual characters.
    #   2. The node type: (CHARACTER, GROUP)
    #   3. The relation type: (VARIANT_OF, COMPOSED_OF)
    #   4. The referent in the relation.  Either a single character when the
    #           relation is VARIANT_OF or a list of component characters.
    def _parse_line(self, line_string):
        split_line = line_string.strip().split(':')

        # Extract the four fields as strings
        id_string = split_line[0]
        type_string = split_line[1]
        relation_string = split_line[2]
        referent_string = split_line[3]

        # Turn the strings into binary

        # 1. The node type
        node_type = _node_type_map[type_string]

        # 2. The node ID
        if node_type == GROUP:
            # The ID is the group ID
            node_id = int(id_string)
        else:
            # The ID is a single Unicode character
            assert(len(id_string) == 1)
            node_id = id_string

        # 3. The type of relation the node represents
        relation_type = _relation_map[relation_string]

        # 4. The referent

        # First case, this character is a variant of a primary
        # character. There should only be one character.
        # The referent in this relation is the primary character.
        if relation_type == VARIANT_OF:
            assert(len(referent_string) == 1)
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
                node_id, node_type, relation_type, referent = self._parse_line(line)
                assert(not node_id in self._decomp_table)
                self._decomp_table[node_id] = (node_id, node_type, relation_type, referent)

    # Returns a tree.
    def decompose(self, ch):
        try:
            record = self._decomp_table[ch]
        except KeyError:
            raise RuntimeError("No decomposition data for " + repr(ch))

        if record[3] == None:
            # This is a simple character that has no components
            return record
        pass

    def __str__(self):
        return str(self._decomp_table)

def is_unicode_kangxi_radical(ch):
    # See http://en.wikipedia.org/wiki/Kangxi_Radicals#Unicode
    return '⼀' <= ch and ch <= '⿕'

def is_unicode_supplemental_radical(ch):
    # See ttp://en.wikipedia.org/wiki/CJK_Radicals_Supplement
    return '⺀' <= ch and ch <= '⻳' 
def is_unicode_radical(ch):
    return is_unicode_kangxi_radical(ch) or is_unicode_supplemental_radical(ch)

def is_unicode_stroke(ch):
    return '㇀' <= ch and ch <= '㇣'
