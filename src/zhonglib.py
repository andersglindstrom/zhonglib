# -*- coding: utf-8 -*-

import os.path
import functools
import operator
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

class CharacterDecomposer:

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
        except KeyError: raise RuntimeError('No decomposition data for ' + repr(ch))

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

import whoosh.analysis
from whoosh.index import create_in, open_dir
from whoosh.fields import *
import string

def parse_dictionary_line(line):
    start = 0
    end = string.find(line, " ", start)
    traditional = line[start:end]
    start = end+1
    end = string.find(line, " ", start)
    simplified = line[start:end]
    start = end+1
    end = string.find(line, "]", start)+1
    pinyin = line[start:end]
    start = end+1
    meaning = line[start:].rstrip()
    return traditional, simplified, pinyin, meaning

# Given a file in the CC-CEDICT format, this function creates a Whoosh
# index that is used later for searching
def create_dictionary(source, destination, english_index=True, verbose=False):
    # Use ID field for Chinese words because they are already tokenized.
    # Using TEXT doesn't work properly because single letter words are ignored.

    if english_index:
        meaning_field = TEXT(stored=True)
    else:
        meaning_field = STORED()

    schema = Schema(traditional=ID(stored=True),
                    simplified=ID(stored=True),
                    pinyin=TEXT(stored=True),
                    meaning=meaning_field)
    if os.path.exists(destination):
        msg = "Dictionary already exists: " + destination
        raise RuntimeError(msg)
    os.mkdir(destination)
    if verbose:
        num_lines = sum(1 for line in open(source))
        line_count = 0
    index = create_in(destination, schema)
    writer = index.writer()
    with codecs.open(source, 'r', encoding='utf-8') as f:
        for line in f:
            if not line[0] == '#':
                trad, simp, pin, mean = parse_dictionary_line(line)
                if verbose:
                    line_count += 1
                    pct_done = 100.0*line_count/num_lines
                    print pct_done, '% done. Added "'+trad+'"'
                writer.add_document(
                        traditional=trad,
                        simplified=simp,
                        pinyin=pin,
                        meaning=mean)
    if verbose:
        print "Committing. This may take a couple of minutes."
    writer.commit()

from whoosh.query import Term

class Entry:

    def __init__(self, traditional, simplified, pinyin, raw_meaning):
        self.traditional = traditional
        self.simplified = simplified
        self.pinyin = pinyin
        self.raw_meaning = raw_meaning
        self.meaning = []
        self.traditional_measure_words = []
        self.simplified_measure_words = []
        self._extract_parts(raw_meaning)

    def _extract_parts(self, raw_meaning):
        parts = raw_meaning[1:-1].split('/')
        for part in parts:
            if not part.startswith('CL:'):
                self.meaning.append(part)
            else: # is a measure word
                part = part[3:] # Remove 'CL:'
                part = part[:part.find('[')]    # Remove pinyin
                if len(part) == 1:
                    self.traditional_measure_words.append(part)
                    self.simplified_measure_words.append(part)
                else:
                    assert(part[1] == '|')
                    self.traditional_measure_words.append(part[0])
                    self.simplified_measure_words.append(part[2])

class Dictionary:

    # dict_path is path to dictionary created previously by 
    # 'create_dictionary'

    def __init__(self, dict_path):
        self._index =  open_dir(dict_path)

    def find(self, search_string):
        with self._index.searcher() as searcher:
            query = Term("traditional", search_string) \
                        | Term('simplified', search_string) \
                        | Term('meaning', search_string)
            results = searcher.search(query)
            return_value = []
            for result in results:
                return_value.append(Entry(
                    result['traditional'],
                    result['simplified'],
                    result['pinyin'],
                    result['meaning']
                ));
            return return_value

__standard_dictionary_path = os.path.join(
    os.path.dirname(__file__),
    'zhonglib-data',
    'dictionary'
)

if os.path.exists(__standard_dictionary_path):
    __standard_dictionary = Dictionary(os.path.join(__standard_dictionary_path))

def standard_dictionary():
    return __standard_dictionary

def find(word):
    return __standard_dictionary.find(word)

__standard_decomposer = CharacterDecomposer(os.path.join(
    os.path.dirname(__file__),
    'zhonglib-data',
    'decomposition-data.txt'
))

def decompose_character(character, flatten=True, stopAtStrokes=True):
    decomposition = __standard_decomposer.decompose(character)
    if flatten:
        decomposition = flatten_decomposition(decomposition, stopAtStrokes)
    return decomposition

def flatten_one_level_down(record, stopAtStrokes=True):
    if record_type(record) == CHARACTER:
        return record_id(record)
    assert record_type(record) == GROUP
    children = record_referent(record)
    result = []
    for child in children:
        result += flatten_one_level_down(child)
    return result

def any_are_strokes(characters):
    for c in characters:
        if is_unicode_stroke(c):
            return True
    return False

def flatten_decomposition(record, stopAtStrokes=True):
    if record_type(record) == CHARACTER and record_referent(record) == None:
        return []
    if record_type(record) == CHARACTER and record_relation_type(record) == VARIANT_OF:
        return list(flatten_one_level_down(record_referent(record)))
    children = record_referent(record)
    result = []
    for child in children:
        result += flatten_one_level_down(child)
    if len(result) > 0 and stopAtStrokes and any_are_strokes(result):
        result = []
    return result

def decompose_word(word):
    return [ch for ch in word]

def decompose(text, stopAtStrokes=True):
    if len(text) == 1:
        return decompose_character(text, stopAtStrokes)
    else:
        return decompose_word(text)
