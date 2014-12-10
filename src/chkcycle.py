#!/usr/bin/env python

import os
import sys
import zhonglib

if len(sys.argv) != 2:
    print 'usage:', sys.argv[0], '<decomposition file>'
    sys.exit(1)

decomposition_file = sys.argv[1]

if not os.path.exists(decomposition_file):
    print 'File not found:', decomposition_file
    sys.exit(1)

decomposer = zhonglib.CharacterDecomposer(decomposition_file)

result = zhonglib.check_decomposer_for_cycles(decomposer)

if len(result) == 0:
    sys.exit(0)

for msg in result:
    print msg
sys.exit(1)
