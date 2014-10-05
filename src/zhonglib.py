# -*- coding: utf-8 -*-

import os.path
import functools
import operator
import codecs
import string

# Constants

# Node type
CHARACTER   = 1
GROUP       = 2

# Relation type
COMPOSED_OF = 3
VARIANT_OF  = 4

# Traditional or simplified character sets

SIMPLIFIED = 0x0001
TRADITIONAL = 0x0002

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

class ZhonglibException(Exception):

    def __init__(self, message):
        self.message = message

    def __unicode__(self):
        return self.message

    def __str__(self):
        return unicode(self).encode('utf-8')

class DecompositionError(ZhonglibException):

    def __init__(self, text):
        self.text = text

    def __unicode__(self):
        return u'Unable to decompose "%s"'%self.text

    def __str__(self):
        return unicode(self).encode('utf-8')

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
            raise ZhonglibException(msg)

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
        except KeyError: raise ZhonglibException('No decomposition data for ' + repr(ch))

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

# For all the following classifications, see the following overview page:
#http://en.wikipedia.org/wiki/Han_unification

def is_unified_character(ch):
    return unichr(0x4E00) <= ch and ch <= unichr(0x9FFF)

def is_unified_extension_A_character(ch):
    return unichr(0x3400) <= ch and ch <= unichr(0x4DBF)

def is_unified_extension_B_character(ch):
    return unichr(0x20000) <= ch and ch <= unichr(0x2A6DF)

def is_unified_extension_C_character(ch):
    return unichr(0x2A700) <= ch and ch <= unichr(0x2B73F)

def is_unified_extension_D_character(ch):
    return unichr(0x2B740) <= ch and ch <= unichr(0x2B81F)

def is_supplemental_radical(ch):
    # See http://en.wikipedia.org/wiki/CJK_Radicals_Supplement
    return unichr(0x2E80) <= ch and ch <= unichr(0x2EFF)

def is_kangxi_radical(ch):
    # See http://en.wikipedia.org/wiki/Kangxi_Radicals#Unicode
    return unichr(0x2F00) <= ch and ch <= unichr(0x2FDF) 

def is_description_character(ch):
    return unichr(0x2FF0) <= ch and ch <= unichr(0x2FFF)

def is_symbol_or_punctuation(ch):
    return unichr(0x3000) <= ch and ch <= unichr(0x303F)

def is_stroke(ch):
    return unichr(0x31C0) <= ch and ch <= unichr(0x31EF)

def is_enclosed_letter_or_month(ch):
    return unichr(0x3200) <= ch and ch <= unichr(0x32FF)

def is_compatibility_character(ch):
    return unichr(0x3300) <= ch and ch <= unichr(0x33FF)

def is_compatibility_ideograph(ch):
    return unichr(0xF900) <= ch and ch <= unichr(0xFAFF)

def is_compatibility_form(ch):
    return unichr(0xFE30) <= ch and ch <= unichr(0xFE4F)

def is_compatibility_ideograph_supplement(ch):
    return unichr(0x2F800) <= ch and ch <= unichr(0x2FA1F)

def is_cjk_character(ch):
    return is_unified_character(ch)\
        or is_unified_extension_A_character(ch)\
        or is_unified_extension_B_character(ch)\
        or is_unified_extension_C_character(ch)\
        or is_unified_extension_D_character(ch)\
        or is_supplemental_radical(ch)\
        or is_kangxi_radical(ch)\
        or is_description_character(ch)\
        or is_symbol_or_punctuation(ch)\
        or is_stroke(ch)\
        or is_enclosed_letter_or_month(ch)\
        or is_compatibility_character(ch)\
        or is_compatibility_ideograph(ch)\
        or is_compatibility_form(ch)\
        or is_compatibility_ideograph_supplement(ch)

def is_radical(ch):
    return is_kangxi_radical(ch) or is_supplemental_radical(ch)

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
        raise ZhonglibException(msg)
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
from whoosh.query import NullQuery

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
                measure_words = [mw.strip().rstrip() for mw in part.split(',')]
                for mw in measure_words:
                    mw = mw[:mw.find('[')]    # Remove pinyin
                    if len(mw) == 1:
                        # There's only one character.  It is used in both
                        # traditional and simplified character sets.
                        self.traditional_measure_words.append(mw)
                        self.simplified_measure_words.append(mw)
                    else:
                        assert(len(mw) == 3)
                        assert(mw[1] == '|')
                        # There are two characters.  One for traditional and
                        # one for simplified. They are separated by | character.
                        self.traditional_measure_words.append(mw[0])
                        self.simplified_measure_words.append(mw[2])

class Dictionary:

    # dict_path is path to dictionary created previously by 
    # 'create_dictionary'

    def __init__(self, dict_path):
        self._index =  open_dir(dict_path)

    # Looks for entries in the dictionary.
    # 'character_set' is TRADITIONAL, SIMPLIFIED, (TRADITIONAL | SIMPLIFIED)
    # if both are required, or 0 if neither is. If 'include_english' is True,
    # the English text will be searched too.
    # At least of of 'character_set' or 'include_english' must be provided.

    def find(self, search_string, character_set=0, include_english=False):
        assert character_set or include_english
        with self._index.searcher() as searcher:
            query = NullQuery()
            if character_set & TRADITIONAL:
                query |= Term("traditional", search_string)
            if character_set & SIMPLIFIED:
                query |= Term('simplified', search_string)
            if include_english:
                query |= Term('meaning', search_string)
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

    def __contains__(self, key):
        with self._index.searcher() as searcher:
            # Documentation for Whoosh says 'in'
            # operator can be used on the searcher
            # to look for the key but it didn't work
            # for me.
            query = Term("traditional", key) \
                    | Term('simplified', key)
            results = searcher.search(query)
            return len(results) > 0


__standard_dictionary_path = os.path.join(
    os.path.dirname(__file__),
    'zhonglib-data',
    'dictionary'
)

if os.path.exists(__standard_dictionary_path):
    __standard_dictionary = Dictionary(os.path.join(__standard_dictionary_path))

def standard_dictionary():
    return __standard_dictionary

def find(word, character_set=0, include_english=False):
    return __standard_dictionary.find(word, character_set, include_english)

#==============================================================================
# Character frequency data

def read_frequency_table(file_name):
    result = {}
    frequency_total = 0
    with codecs.open(file_name, 'r', encoding='utf-8') as f:
        for line in f:
            words = line.split(' ')
            assert len(words) == 2
            word = words[0]
            frequency = int(words[1])
            result[word] = frequency
            frequency_total += frequency
    # Normalise to 100
    for key, value in result.iteritems():
        result[key] = value*100.0/frequency_total
    return result

def read_standard_frequency_tables():
    result = {}
    traditional_frequency_path = os.path.join(
        os.path.dirname(__file__),
        'zhonglib-data',
        'traditional-frequencies.txt'
    )
    if os.path.exists(traditional_frequency_path):
       result.update(read_frequency_table(traditional_frequency_path))

    simplified_frequency_path = os.path.join(
        os.path.dirname(__file__),
        'zhonglib-data',
        'simplified-frequencies.txt'
    )
    if os.path.exists(simplified_frequency_path):
        result.update(read_frequency_table(simplified_frequency_path))

    return result

_standard_frequency_table = read_standard_frequency_tables()

#==============================================================================
# Decomposition 
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
        if is_stroke(c):
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
    result = []
    for ch in word:
        if is_cjk_character(ch):
            result += ch
    return result

def decompose(text, stopAtStrokes=True):
    if len(text) == 1:
        return decompose_character(text, stopAtStrokes)
    else:
        segments = segment(text)
        if len(segments) == 1:
            word = segments[0]
            return decompose_word(word)
        else:
            return segments

def extract_cjk(text):
    state = 1
    idx = 0
    pattern = ''
    words = []
    while idx <= len(text):
        if idx < len(text):
            ch = text[idx]
        else:
            ch = None
        idx += 1
        if state == 1:  # Non CJK characters
            if ch == None:  # We've finished processing the text.
                pass
            elif is_cjk_character(ch):
                word = ch
                state = 2
                pattern += '%s'
            else:
                pattern += ch
        elif state == 2:    # CJK characters
            if ch == None:  # We've finished processing the text.
                words.append(word)
            elif is_cjk_character(ch):
                word += ch
            else:
                words.append(word)
                pattern += ch
                state = 1
    return pattern, tuple(words)

def _parse_one_cedict_pinyin(text):
    if text == 'xx5':
        # This is a special CEDICT indicator that there is no pinyin for
        # the given word.
        return None
    if text[-1].isdigit():
        syllable = text[0:-1]
        tone = int(text[-1])
        if tone == 5:
            tone = 0
    else:
        syllable = text
        tone = 0
    syllable = syllable.replace(u'u:',u'ü').replace(u'U:',u'Ü') 
    return (syllable, tone)

def parse_cedict_pinyin(text):
    if text[0] != '[' or text[-1] != ']':
        raise ZhonglibException(text + ' is not in CEDICT pinyin format.')
    elements = text[1:-1].split(' ')
    return map(_parse_one_cedict_pinyin, elements)

# Pinyin vowels are ordered (a,o,e,i,u,ü). It's not significant for this code.
_vowels = frozenset({'a','o','e','i','u',u'ü','A','O','E','I','U',u'Ü'})


_tone_table = {
    u'a':(u'a',u'ā',u'á',u'ǎ',u'à'),
    u'o':(u'o',u'ō',u'ó',u'ǒ',u'ò'),
    u'e':(u'e',u'ē',u'é',u'ě',u'è'),
    u'i':(u'i',u'ī',u'í',u'ǐ',u'ì'),
    u'u':(u'u',u'ū',u'ú',u'ǔ',u'ù'),
    u'ü':(u'ü',u'ǖ',u'ǘ',u'ǚ',u'ǜ'),
    u'A':(u'A',u'Ā',u'Á',u'Ǎ',u'À'),
    u'O':(u'O',u'Ō',u'Ó',u'Ǒ',u'Ò'),
    u'E':(u'E',u'Ē',u'É',u'Ě',u'È'),
    u'I':(u'I',u'Ī',u'Í',u'Ǐ',u'Ì'),
    u'U':(u'U',u'Ū',u'Ú',u'Ǔ',u'Ù'),
    u'Ü':(u'U',u'Ǖ',u'Ǘ',u'Ǚ',u'Ǜ')
}

def is_vowel(ch):
    return ch in _vowels

# See http://en.wikipedia.org/wiki/Pinyin#Rules_for_placing_the_tone_mark
# and http://en.wikipedia.org/wiki/Pinyin_table

def format_pinyin(syllable, tone):

    if syllable == 'r':
        # Special case for retroflex r (兒), which should represented
        # as ('r', 0).
        assert tone == 0
        return 'r'

    initial = u''
    final = u''

    state = 1
    vowel_count = 0

    idx = 0
    a_idx = None
    e_idx = None
    o_idx = None

    # In the first part, extract the initial and final parts of the
    # syllable.  Also, keep track of where various vowels are located
    # and the total vowel count.
    #
    # In the second part, these are used to apply formatting rule as
    # specified on the wiki page above. The version preceded by 'Worded
    # differently,' is used.

    # Part 1
    idx = 0
    while idx < len(syllable): 
        ch = syllable[idx]
        if state == 1:  # Getting the initial
            if not is_vowel(ch):
                initial += ch
            else:
                state = 2
        # State may have just changed above so can't 
        # use 'elif'
        if state == 2:
            final += ch
            if is_vowel(ch):
                vowel_count += 1
            if ch == 'a' or ch == 'A':
                a_idx = idx
            if ch == 'e' or ch == 'E':
                e_idx = idx
            if ch == 'o' or ch == 'O':
                o_idx = idx
        idx += 1

    # Part 2. Calculate the vowel to get the tone
    if vowel_count == 1:
        # Vowel must be first letter of final part
        vowel_idx = len(initial)
    else:
        # In the following, the idx could point to either a lower or upper
        # case character so we have to use that character rather than a
        # literal.
        if a_idx != None:
            vowel_idx = a_idx
        elif e_idx != None:
            vowel_idx = e_idx
        elif o_idx != None:
            vowel_idx = o_idx
        else:
            # Otherwise, second vowel takes the mark
            # The second vowel must be the second letter of the final part.
            vowel_idx = len(initial)+1

    # Lood up the toned vowel
    try:
        toned_vowel = _tone_table[syllable[vowel_idx]][tone]
    except IndexError:
        print 'syllable: "%s" vowel_idx: %s'%(syllable,vowel_idx)
        raise

    # Put it all together again
    return syllable[0:vowel_idx] + toned_vowel + syllable[vowel_idx+1:]

# A pinyin sequence is a sequence of pairs and None. A pair contains
# a syllable and a tone number.  If None, it means that there is no
# pinyin available. This happens in the CEDICT dictionary sometimes for
# Unicode supplemental radicals and Korean characters.
def format_pinyin_sequence(tuples):
    try:
        result = u''
        for t in tuples:
            if t == None:
                result += 'None'
            else:
                result += format_pinyin(t[0], t[1])
        return result
    except IndexError:
        print 'tuples: %s'%tuples
        raise

def list_to_uc(l):
    result = u''
    result += u'['
    for i in xrange(len(l)):
        if i > 0:
            result += u', '
        if type(l[i]) == list:
            result += list_to_uc(l[i])
        else:
            result += unicode(l[i])
    result += u']'
    return result

# For segmentation algorithm see the following:
# http://technology.chtsai.org/mmseg/
# A copy of that page is kept in the doc directory.

def print_debug(depth, *args):
    print ' ' * depth,
    for a in args:
        print a,
    print

# A chunk is a list of matched words.
# This function looks at the given text starting from the starting index.
# It will return a list of all chunks that can be found from that position.
# The chunks will be of the requested length unless there is not enough text
# left to do so. In that case, some chunks may be shorter. If the algorithm
# gets to a point where there is still text left but it cannot find a matching
# word, it will fail.  It does this by returning an empty list.
#
# This is a recursive function. The last two parameters are used for recursion
# and should not be used by client code.
def get_chunks(text, start_idx, dictionary, max_key_length, chunk_length=3, depth=0):
    #print_debug(depth, 'get_chunks: enter')
    #print_debug(depth, 'text: "%s"'%text)
    if chunk_length == 0:
        #print_debug(depth, 'get_chunks: exit(1)')
        # A list length of 0 mean there is only one possible list, the empty
        # list. This is not the same as no chunk list. See below when there
        # are no matching words.
        return [[]]

    # Get first words
    first_words = []
    last_idx = min(len(text), start_idx+max_key_length)

    if start_idx == last_idx:
        # No more input left
        #print_debug(depth, 'no input left')
        # If there is no more input, the empty list is the only possible chunk
        # list. This is not the same as no chunk list. See below when there
        return [[]]

    # Find all words at the start of the input up to the max key length
    # and also not exceeding the available input.
    #print_debug(depth, 'start_idx: %s last_idx: %s'%(start_idx,last_idx))
    for end_idx in xrange(start_idx, last_idx+1):
        #print_debug(depth, 'end_idx:',end_idx)
        word = text[start_idx:end_idx]
        #print_debug(depth, "word: '%s'"%word)
        if word in dictionary:
            first_words.append(word)

    if len(first_words) == 0:
        #print_debug(depth, 'get_chunks: exit(2)')
        # None of the input could be matched to any words. There are no
        # chunk lists.
        return []

    # For every possible word at the start of the input, find all the possible
    # chunk lists for the remaining input.  Once that's done, for every following
    # chunk list, create a new one that prepends the first word.
    result = []
    #print_debug(depth, 'first_words:', list_to_uc(first_words))
    for first_word in first_words:
        tails = get_chunks(
            text,
            start_idx+len(first_word),
            dictionary,
            max_key_length,
            chunk_length-1,
            depth+1
        )
        #print_debug(depth, "first_word: '%s' tails: %s"%(first_word,list_to_uc(tails)))
        for tail in tails:
            result.append([first_word] + tail)

    #print_debug(depth, 'get_chunks: exit(3)')
    return result

# The length of a chunk is the total number of characters in the chunk. It is
# not just the length of the list.
def chunk_length(chunk_list):
    return reduce(lambda total, chunk: total+len(chunk), chunk_list, 0)

def get_next_word(text, idx, dictionary, max_key_length):
    
    #print 'get_next_word: text=%s idx=%s'%(text,idx)
    candidates = get_chunks(text, idx, dictionary, max_key_length)

    #print 'get_next_word: candidates=', list_to_uc(candidates)
    if len(candidates) == 0:
        return None

    if len(candidates) == 1:
        # No ambiguities.  Choose the first chunk of the only candidate.
        return candidates[0][0]

    # There is more than one candidate. Use Rule 1, which is to pick the
    # chunk with biggest number of characters in it and then to pick the
    # first word.
    max_length = max(map(lambda l: chunk_length(l), candidates))
    candidates = filter(lambda l: chunk_length(l) == max_length, candidates)

    if len(candidates) == 1:
        # No ambiguities.  Choose the first chunk of the only candidate.
        return candidates[0][0]

    # All candidates have the same number of characters.  Now choose the one
    # with the highest average word length.  Becuase they all have the same
    # number of characters, this is the same as choosing the chunk list with
    # the smallest number of words in it.

    min_avg_length = min(map(lambda l: len(l), candidates))
    candidates = filter(lambda l: len(l) == min_avg_length, candidates)

    if len(candidates) == 1:
        # No ambiguities.  Choose the first chunk of the only candidate.
        return candidates[0][0]

    #print 'get_next_word: ambiguity not resolved, candidates=',list_to_uc(candidates)
    return None

# Segments a contiguous string of characters; that is, it must not contain
# any punctuation or whitespace.
def segment_contiguous(text, dictionary, max_key_length):
    result = []
    idx = 0
    #print 'text:',text
    while idx < len(text):
        next_word = get_next_word(text, idx, dictionary, max_key_length)
        #print 'next_word:',next_word
        if next_word == None:
            raise DecompositionError(text)
        result.append(next_word)
        idx += len(next_word)
    return result

def split_into_contiguous(text):
    result = []
    current_word = ''
    state = 1
    for ch in text:
        if state == 1:
            if ch.isspace()\
            or is_symbol_or_punctuation(ch)\
            or ch in string.punctuation:
                state = 2
                result.append(current_word)
                current_word = ''
            else:
                current_word += ch
        elif state == 2:
            if not ch.isspace()\
            and not is_symbol_or_punctuation(ch)\
            and not ch in string.punctuation:
                current_word += ch
                state = 1
    if len(current_word) > 0:
        result.append(current_word)
    return result

# Segments a piece of text.  Whitespace and punctuation are used as the
# primary segmentation points.  After that, each contiguous string of
# characters is segmented using 'segment_contiguous.'

def segment(text, dictionary=None, max_key_length=None):
    if dictionary == None:
        dictionary = standard_dictionary()
        max_key_length = 9  # Fix this. It should be based on dictionary contents.
    result = []
    for c in split_into_contiguous(text):
        result += segment_contiguous(c, dictionary, max_key_length)
    return result
