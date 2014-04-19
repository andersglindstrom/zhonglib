#!/usr/bin/env python3.3
from __future__ import print_function

import codecs

# This is a quick script to convert cjk-decomp-0.4.0.txt into zhonglib internal decomposition file format

def node_type(node_id):
    if len(node_id) == 1:
        return 'z'
    else:
        return 'g'

def parse_decomp_string(decomp_string):
    start = decomp_string.find('(') + 1
    end = decomp_string.find(')')
    return decomp_string[start:end]

def process_line(line):
    node_id, colon, decomp_string = line.partition(':')
    record_node_type = node_type(node_id)
    relation_type = 'c' # All decompositions. No variants.
    decomp_data = parse_decomp_string(decomp_string)
    print(node_id,record_node_type,'c', decomp_data, sep=':')

with codecs.open('cjk-decomp-0.4.0.txt', encoding='utf-8') as f:
    for line in f:
        process_line(line)
