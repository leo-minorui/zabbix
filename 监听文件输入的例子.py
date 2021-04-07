# -*- coding: utf-8 -*-

def tail(filename)
    f = open('file',encoding='utf-8')
    while True:
        line = f.readline()
        if line.strip():
            yield line.strip()

g = tail('file')
for i in g:
    if 'python' in i:
        print('***',i)