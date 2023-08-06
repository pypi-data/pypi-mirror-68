#!python
"""
This file is part of PyMMB - The crossplatform MMB library and toolset
If you don't use MMC Flash cards in a BBC Microcomputer, this is unlikely
to be a lot of use to you!
"""

import PyMMB
import sys

if __name__ == '__main__':
    if len(sys.argv) < 5:
        print "Syntax: %s <BEEB.MMB> (<disc_name> | <disc_id>) <dir>.<file> <unix filename>" % sys.argv[0]
        sys.exit()
    MMB = PyMMB.mmb.mmb(sys.argv[1])
    try:
        DFS = MMB.get_disc(int(sys.argv[2]))
    except:
        DFS = MMB.find_disc(sys.argv[2])
    d, n = sys.argv[3].split(".")
    DFS.create_file(d, n, open(sys.argv[4]).read(999999()
