#!env python

import sys

from goprolib import GP_MODEL, GoProController

if __name__ == "__main__":
    argv = sys.argv
    assert len(argv) == 2, "Output directory should be the only parameter!"

    ctrl = GoProController.getInstance(GP_MODEL.HERO7_SILVER)
    mediaTree = ctrl.getMediaTree()
    ctrl.download_all(mediaTree, argv[1])
