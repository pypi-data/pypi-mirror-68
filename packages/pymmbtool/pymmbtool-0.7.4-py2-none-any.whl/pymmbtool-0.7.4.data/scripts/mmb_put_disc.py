#!python
"""
This file is part of PyMMB - The crossplatform MMB library and toolset
If you don't use MMC Flash cards in a BBC Microcomputer, this is unlikely
to be a lot of use to you!
"""

import PyMMB
import sys

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Syntax: %s <BEEB.MMB> (<disc_name> | <disc_id>) <disc.ssd>" % sys.argv[0]
        sys.exit()
    MMB = PyMMB.mmb.mmb(sys.argv[1])
    try:
        MMB.get_disc(int(sys.argv[2])).read_from(sys.argv[3])
        MMB.write_catalog()
    except:
        raise
        MMB.find_disc(sys.argv[2]).read_from(sys.argv[3])
