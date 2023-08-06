#!python
"""
This file is part of PyMMB - The crossplatform MMB library and toolset
If you don't use MMC Flash cards in a BBC Microcomputer, this is unlikely
to be a lot of use to you!
"""

import PyMMB
import sys
import math

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print "Syntax: %s <disc.ssd>" % sys.argv[0]
        sys.exit()
    DFS = PyMMB.dfs.dfs(sys.argv[1])
    DFS.compact()
    end = 2
    for dfsfile in DFS.files:
        this_end = dfsfile.start_sector + math.ceil(dfsfile.length / 256)
        if this_end > end:
            end = this_end
    print "This disc has %s bytes free" % ((DFS.sectors - end) * 256)
