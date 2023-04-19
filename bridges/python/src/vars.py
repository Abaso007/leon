#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
from json import loads

with open(os.path.join(os.getcwd(), 'package.json'), 'r', encoding = 'utf8') as packagejsonfile:
    packagejson = loads(packagejsonfile.read())
useragent = 'Leon-Personal-Assistant/' + packagejson['version']
