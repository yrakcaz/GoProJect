import collections
import datetime
import requests
import shutil

import PIL.ExifTags
import PIL.Image

from enum import Enum

class GP_MODEL(Enum):
    HERO7_SILVER = 1
    # TODO add more models!

class GP_COMMAND(Enum):
    MODE_PHOTO = 1
    TRIGGER_START = 2
    # TODO add more commands!

class GP_SETTING(Enum):
    AUTO_OFF_NEVER = 1
    # TODO add more settings!

class GoProController(object):
    __instance = None

    @staticmethod
    def getInstance(model):
        if GoProController.__instance == None:
            GoProController(model)
        return GoProController.__instance

    def __init__(self, model):
        if GoProController.__instance != None:
             raise Exception("This class is a singleton!")
        else:
            GoProController.__instance = self

        self.model_ = model

    def baseUrl(self):
        if self.model_ == GP_MODEL.HERO7_SILVER:
            return "http://10.5.5.9/"
        # TODO add more models!
        else:
            assert False, "Unknown GoPro model!"

    def gpControl(self):
        if self.model_ == GP_MODEL.HERO7_SILVER:
            return self.baseUrl() + "gp/gpControl/"
        # TODO add more models!
        else:
            assert False, "Unknown GoPro model!"

    def gpCommand(self, command):
        if self.model_ == GP_MODEL.HERO7_SILVER:
            ret = self.gpControl() + "command/"
            if command == GP_COMMAND.MODE_PHOTO:
                return ret + "mode?p=1"
            elif command == GP_COMMAND.TRIGGER_START:
                return ret + "shutter?p=1"
            # TODO add more commands!
            else:
                assert False, "Unknown GoPro command!"
        # TODO add more models!
        else:
            assert False, "Unknown GoPro model!"

    def gpSetting(self, setting):
        if self.model_ == GP_MODEL.HERO7_SILVER:
            ret = self.gpControl() + "setting/"
            if setting == GP_SETTING.AUTO_OFF_NEVER:
                return ret + "59/0"
            # TODO add more commands!
            else:
                assert False, "Unknown GoPro command!"
        # TODO add more models!
        else:
            assert False, "Unknown GoPro model!"

    def gpMediaList(self):
        if self.model_ == GP_MODEL.HERO7_SILVER:
            return self.baseUrl() + "gp/gpMediaList/"
        # TODO add more models!
        else:
            assert False, "Unknown GoPro model!"

    def gpDownload(self, dirname, filename):
        if self.model_ == GP_MODEL.HERO7_SILVER:
            return self.baseUrl() + "videos/DCIM/" + dirname + "/" + filename
        # TODO add more models!
        else:
            assert False, "Unknown GoPro model!"

    def request(self, url, stream=False):
        r = None
        while True:
            r = requests.get(url, stream=stream)
            if r.status_code == 200:
                break
        assert r.status_code == 200
        print("{}: {}: {}".format(datetime.datetime.now(), url, r))
        return r

    def getMediaTree(self):
        url = self.gpMediaList()
        json = self.request(url).json()
        l = json["media"]
        ret = collections.defaultdict(list)
        for e in l:
            dirname = e["d"]
            for f in e["fs"]:
                ret[dirname].append(f["n"])
        return ret

    def getDiffMediaTree(self, orig):
        new = self.getMediaTree()
        ret = collections.defaultdict(list)
        for k, v in new.iteritems():
            if k not in orig:
                ret[k] = v
            else:
                for e in v:
                     if e not in orig[k]:
                          ret[k].append(e)
        return ret

    def getDateTime(self, img):
        img = PIL.Image.open(img)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
        }
        return exif["DateTime"]

    def download(self, dirname, filename, outpath):
        url = self.gpDownload(dirname, filename)
        r = self.request(url, stream=True)
        with open(outpath + filename, 'wb', 0) as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
            f.flush()
        date = self.getDateTime(outpath + filename)
        name = date.replace(' ', '').replace(':', '') + ".JPG"
        shutil.move(outpath + filename, outpath + name)

    def download_all(self, mediaTree, outpath):
        for k, v in mediaTree.iteritems():
            for e in v:
                self.download(k, e, outpath)
