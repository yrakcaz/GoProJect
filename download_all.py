#!env python

import collections
import datetime
import requests
import shutil

GOPRO = "http://10.5.5.9/"
GP_MEDIALIST = GOPRO + "gp/gpMediaList"
GP_DOWNLOAD = GOPRO + "videos/DCIM/"

def request(command, stream=False):
    resp = requests.get(command, stream=stream)
    print("{}: {}: {}".format(datetime.datetime.now(), command, resp))
    return resp

def getMediaTree():
    json = request(GP_MEDIALIST).json()
    l = json["media"]
    ret = collections.defaultdict(list)
    for e in l:
        dirname = e["d"]
        for f in e["fs"]:
            ret[dirname].append(f["n"])
    return ret

def download(url, path):
   r = None
   while True:
      r = request(url, stream=True)
      if r.status_code == 200:
         break
   assert r.status_code == 200
   with open(path, 'wb') as f:
       r.raw.decode_content = True
       shutil.copyfileobj(r.raw, f)

if __name__ == "__main__":
   for k, v in getMediaTree().iteritems():
      for e in v:
	download(GP_DOWNLOAD + k + "/" + e, e)
         
           
