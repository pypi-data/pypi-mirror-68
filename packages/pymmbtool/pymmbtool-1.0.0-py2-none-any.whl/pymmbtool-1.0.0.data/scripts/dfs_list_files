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
        print "Syntax: %s <disc.ssd>" % sys.argv[0]
        sys.exit()
    DFS = PyMMB.dfs.dfs(sys.argv[1])
    for f in DFS.files:
        print f.fullname
