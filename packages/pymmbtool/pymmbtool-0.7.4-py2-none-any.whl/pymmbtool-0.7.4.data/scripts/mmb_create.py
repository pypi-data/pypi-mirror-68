#!python
"""
This file is part of PyMMB - The crossplatform MMB library and toolset
If you don't use MMC Flash cards in a BBC Microcomputer, this is unlikely
to be a lot of use to you!
"""

import PyMMB
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Syntax: %s <BEEB.MMB> <entry count>" % sys.argv[0]
        sys.exit()
    MMB = PyMMB.mmb.mmb.create(sys.argv[1], entries = int(sys.argv[2]))
