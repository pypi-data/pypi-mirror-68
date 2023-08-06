#!python
"""
This file is part of PyMMB - The crossplatform MMB library and toolset
If you don't use MMC Flash cards in a BBC Microcomputer, this is unlikely
to be a lot of use to you!
"""

import PyMMB
import sys

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Syntax: %s <BEEB.MMB> [<disc_name> | <disc_id>]" % sys.argv[0]
        sys.exit()
    MMB = PyMMB.mmb.mmb(sys.argv[1])
    if len(sys.argv) == 2:
        print MMB.catalog(True)
        sys.exit()
    try:
        print MMB.get_disc(int(sys.argv[2])).catalog()
    except:
        print MMB.find_disc(sys.argv[2]).catalog()
