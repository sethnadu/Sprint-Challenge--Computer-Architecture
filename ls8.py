#!/usr/bin/env python3

"""Main."""

import sys


from cpu import *

cpu = CPU()

# Check for what arguement of files be ran
if len(sys.argv) != 2:
    print("Usage: file.py filename", file=sys.stderr)
    sys.exit(1)
else:
    fileName = sys.argv[1]


cpu.load(fileName)
cpu.run()
cpu.trace()
print("RAM", cpu.ram)
print("REG TOTAL", cpu.reg)