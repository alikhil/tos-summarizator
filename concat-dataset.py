#!/bin/python

from os import listdir
from os.path import isfile, join

dateset_dir = "dataset"

files = [join(dateset_dir,f) for f in listdir(dateset_dir) if isfile(join(dateset_dir, f))]

with open("total.txt", "w") as result_stream:
    for f in files:
        with open(f) as inp:
            result_stream.write(inp.read())
