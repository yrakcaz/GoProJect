#!env python

import argparse
import sys
import time

from daemon import Daemon
from goprolib import GP_COMMAND, GP_MODEL, GP_SETTING, GoProController

class Runner(Daemon):
    def run(self, interval, numClicks, outpath):
        ctrl = GoProController.getInstance(GP_MODEL.HERO7_SILVER)

        ctrl.request(ctrl.gpSetting(GP_SETTING.AUTO_OFF_NEVER))
        ctrl.request(ctrl.gpCommand(GP_COMMAND.MODE_PHOTO))

        mediaTree = ctrl.getMediaTree()

        i = 0
        while True:
            if numClicks > -1 and i == numClicks:
                break

            ctrl.request(ctrl.gpCommand(GP_COMMAND.TRIGGER_START))
            diffTree = ctrl.getDiffMediaTree(mediaTree)
            ctrl.download_all(diffTree, outpath)
            mediaTree = ctrl.getMediaTree()

            time.sleep(interval)
            i += 1

def parseArgs(argv):
    parser = argparse.ArgumentParser(
            prog="timelapse.py",
            description="Daemon that click pics on connected GoPro every INTERVAL seconds." )

    parser.add_argument("--interval", "-i", action="store", type=int,
                        help="interval in seconds between two clicks (default=60)" )
    parser.add_argument("--numClicks", "-n", action="store", type=int,
                        help="number of pics to click (default=unlimited)" )

    parser.add_argument("--pidfile", "-p", action="store", type=str,
                        help="path to pidfile (default=/tmp/timelapse.pid)")
    parser.add_argument("--logfile", "-l", action="store", type=str,
                        help="path to logfile (default=/home/pi/timelapse.log)")
    parser.add_argument("--outpath", "-o", action="store", type=str,
                        help="path to directory to download pics (default=/home/pi/Pictures)")

    parser.add_argument("action", nargs="?", choices=("start", "restart", "stop"),
                        help="start, restart or stop the daemon")

    args = parser.parse_args(argv)

    if args.interval or args.numClicks or args.pidfile or args.logfile or args.outpath:
        if args.action == "stop":
            parser.error("options allowed only when starting or restarting the daemon")

    return args

if __name__ == "__main__":
    args = parseArgs(sys.argv[1:])

    daemon = Runner(args.pidfile or '/tmp/timelapse.pid',
                    stdout=args.logfile or '/home/pi/timelapse.log',
                    stderr=args.logfile or '/home/pi/timelapse.log')

    if args.action == "start":
        daemon.start(interval=args.interval or 60,
                     numClicks=args.numClicks or -1,
                     outpath=args.outpath or "/home/pi/Pictures/")
    elif args.action == "restart":
        daemon.restart(interval=args.interval or 60,
                       numClicks=args.numClicks or -1,
                       outpath=args.outpath or "/home/pi/Pictures/")
    else:
        daemon.stop()
