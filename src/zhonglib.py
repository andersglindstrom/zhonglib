# -*- coding: utf-8 -*-

import os.path
import codecs

decomp_table = {}

def load_decomposition_data():
    directory = os.path.dirname(__file__)
    data_file = os.path.join(directory, 'data/cjk-decomp-0.4.0.txt') 
    if not os.path.exists(data_file):
        msg = "Decomposition data file does not exist: " + data_file
        raise RuntimeError(msg)
    with codecs.open(data_file, 'r', encoding='utf-8') as f:
        for line in f:
            sep_idx = line.find(':')
            components_start = line.find('(')+1
            components_end = line.rfind(')')
            character = line[:sep_idx]
            components_string = line[components_start:components_end]
            if len(components_string) > 0:
                components = components_string.split(',')
            else:
                components = None
            decomp_table[character] = components

def lazy_load_decomposition_data():
    if len(decomp_table) == 0:
        load_decomposition_data()

# Assumes that 'ch' is encoded in utf-8
# Returns a tree
# Each node is a 2-tuple of (character, list of child nodes)
# Leaf nodes have an empty child list.
def decompose_character(ch, type=None):
    lazy_load_decomposition_data()
    components = decomp_table[ch]
    if components:
        components = [ decompose_character(component) for component in components]
    return (ch, components)

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
