#!/usr/bin/env python

import re, codecs, sys

f = codecs.open(sys.argv[1], 'r', 'utf-8');
o = codecs.open(sys.argv[1]+'.2', 'w', 'utf-8');

for l in f:
    l = re.sub(r'\\u([0-9a-fA-F]+)', lambda m: unichr(int(m.group(1), base=16)), l)
    o.write(l)

