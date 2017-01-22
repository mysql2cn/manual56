#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

files = './filename.txt'
f = open(files, 'r+')
line= f.readline()
for line in f.readlines():
    if line.startswith('#')or not line.split():
        continue
    print line,
    cf = open(line.strip('\n'), 'w')
    cf.close()

f.close()
