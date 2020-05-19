#!/usr/bin/env python3
import sys
from cpu import CPU

try:
    cpu = CPU()
    program = sys.argv[1]
    cpu.load(program)
    cpu.run()
except IndexError:
    print('You forgot to run the argument')