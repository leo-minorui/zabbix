#!/usr/bin/enve python
# -*- coding: utf-8 -*-
# author: Leo
# file: raise
# datetime: 2021/6/18 9:51 上午
# Email: leo.minorui@gmail.com
# ide: PyCharm
a = 4
try:
    import sfasf
except ModuleNotFoundError as e:
    if a == 3:
        raise ValueError('sjfsaf')
    raise