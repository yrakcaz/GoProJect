#!env python

import argparse
import datetime
import glob
import shutil
import sys

from goprolib import getDateTime

def parseArgs(argv):
    parser = argparse.ArgumentParser(
            prog="timelapse.py",
            description="Choose pics and generate timelapse")

    parser.add_argument("--in-path", "-i", action="store", required=True, type=str,
                        help="path to get the pics from")
    parser.add_argument("--out-path", "-o", action="store", required=True, type=str,
                        help="path to put the generated timelapse in")

    parser.add_argument("--interval", "-I", action="store", type=int,
                        help="pick one picture every INTERVAL picture only")
    parser.add_argument("--start", "-s", action="store", type=str,
                        help="only chose picture where time of day is > START (HH:MM)")
    parser.add_argument("--end", "-e", action="store", type=str,
                        help="only chose picture where time of day is > END (HH:MM)")

    return parser.parse_args(argv[1:])

def pick(img, i, interval, start, end):
    if interval is not None and i % interval != 0:
        return False

    if start is None and end is None:
        return True

    timestr = getDateTime(img).split(' ')[1]
    time = datetime.datetime.strptime(timestr, "%H:%M:%S")

    if start is not None:
        start = datetime.datetime.strptime(start, "%H:%M")
        if time < start:
            return False

    if end is not None:
        end = datetime.datetime.strptime(end, "%H:%M")
        if time > end:
            return False

    return True

if __name__ == "__main__":
    args = parseArgs(sys.argv)

    in_path = args.in_path
    out_path = args.out_path
    interval = args.interval
    start = args.start
    end = args.end

    i = 0
    for f in sorted(glob.glob(in_path + "/*")):
        filename = f.split('/')[-1]
        outfile = out_path + '/' + filename
        if pick(f, i, interval, start, end):
            shutil.copyfile(f, outfile)
        i += 1
