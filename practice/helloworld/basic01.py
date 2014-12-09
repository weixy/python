__author__ = 'y981821'
# -*- coding: utf-8 -*-
import os
for root, dirs, files in os.walk('/tmp'):
    print "%s %s %s" % (root, dirs, files)

for x in [i * 10 for i in range(10)]:
    print x
