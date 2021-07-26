#!env python3.9

import argparse
import datetime
import glob
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageFont, ImageDraw

from goprolib import getDateTime

def parseArgs(argv):
    parser = argparse.ArgumentParser(
            prog="timelapse.py",
            description="Select pics and generate timelapse")

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
    parser.add_argument("--timestamp", "-t", action="store_true",
                        help="add timestamp to the pictures based on title (should be YYYYMMDDhhmmss.JPG)")
    parser.add_argument("--ips", action="store", type=int, default=24,
                        help="image per second for the generated timelapse (default=24)")

    return parser.parse_args(argv[1:])

def pick(img, i, interval, start, end):
    if interval is not None and i % interval != 0:
        return False

    if start is None and end is None:
        return True

    timestr = getDateTime(img).split(' ')
    if len(timestr) < 2:
        return False
    time = datetime.datetime.strptime(timestr[1], "%H:%M:%S")

    if start is not None:
        start = datetime.datetime.strptime(start, "%H:%M")
        if time < start:
            return False

    if end is not None:
        end = datetime.datetime.strptime(end, "%H:%M")
        if time > end:
            return False

    return True

def getDateObj(filename):
    date = filename[:-4]
    return datetime.datetime.strptime(date, "%Y%m%d%H%M%S")

def addTimestamp(filename, infile, outfile, startDate):
    img = Image.open(infile)
    font = ImageFont.truetype("fonts/COMIC.TTF", 200)
    dateobj = getDateObj(filename)
    delta = dateobj.date() - startDate.date()
    txt = "{} {} J{}".format(dateobj.date(), dateobj.time(), delta.days)
    edimg = ImageDraw.Draw(img)
    edimg.text((15,15), txt, (237, 230, 211), font=font)
    img.save(outfile)

def progressBar(current, total, text, barLength=20):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent / 100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    print("{} [{}{}] {}% ({}/{})                     ".format(
        text, arrow, spaces, percent, current, total), end='\r')

if __name__ == "__main__":
    args = parseArgs(sys.argv)

    in_path = args.in_path
    out_path = args.out_path
    interval = args.interval
    start = args.start
    end = args.end
    timestamp = args.timestamp
    ips = args.ips

    if interval is not None or start is not None or \
            end is not None:
        i = 0
        files = sorted(glob.glob(in_path + "/*"))
        for f in files:
            progressBar(i, len(files), "Selecting pictures...")
            filename = f.split('/')[-1]
            outfile = out_path + '/' + filename
            if pick(f, i, interval, start, end):
                shutil.copyfile(f, outfile)
            i += 1
        print("\n")
        in_path = out_path

    if timestamp:
        i = 0
        files = sorted(glob.glob(in_path + "/*"))
        for f in sorted(glob.glob(in_path + "/*")):
            progressBar(i, len(files), "Timestamping pictures...")
            filename = f.split('/')[-1]
            infile = in_path + '/' + filename
            outfile = out_path + '/' + filename
            if i == 0:
                startDate = getDateObj(filename)
            addTimestamp(filename, infile, outfile, startDate)
            i += 1
        in_path = out_path

    print("Generating timelapse...")
    subprocess.check_output("ffmpeg -r {} -pattern_type glob -i '{}/*.JPG' -s hd1080 -vcodec libx264 {}/timelapse.mov".format(
                            ips, in_path, out_path), shell=True)
