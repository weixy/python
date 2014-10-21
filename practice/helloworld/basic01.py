__author__ = 'y981821'
# -*- coding: utf-8 -*-
import os
for root, dirs, files in os.walk('/tmp'):
    print "%s %s %s" % (root, dirs, files)
