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
        print "Syntax: %s <disc.ssd> <title> [(40|80)]" % sys.argv[0]
        sys.exit()
    if len(sys.argv) == 3:
        tracks = 80
    else:
        tracks = int(sys.argv[3])
    DFS = PyMMB.dfs.dfs.new(sys.argv[1], title = sys.argv[2], tracks = tracks)
