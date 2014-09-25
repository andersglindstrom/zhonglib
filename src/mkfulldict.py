#!/usr/bin/env python

import os
import sys
import zhonglib

# Generates a dictionary directory from a cc-cedict file.
# The resulting index will be searchable by both Mandarin and English.

if len(sys.argv) != 3:
    print 'usage:', sys.argv[0], '<src> <dst>'
    sys.exit(1)

src = sys.argv[1]
dst = sys.argv[2]

if os.path.exists(dst):
    print 'Dictionary already exists.  Remove before generating.'
    sys.exit(1)

zhonglib.create_dictionary(src, dst, english_index=True, verbose=True)
