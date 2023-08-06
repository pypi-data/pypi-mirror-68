#!/usr/bin/env python3
"""Watches the system clipboard for youtube urls"""
import os
import pyperclip
from pyperclip import waitForNewPaste
import queue
import subprocess
import threading
import time
import sys

from ccaconfig.config import ccaConfig
import ccalogging

import ccacb

ccalogging.setConsoleOut()
ccalogging.setInfo()
log = ccalogging.log

appname = "ytcb"


def getUrl(cfg, url):
    os.chdir(cfg["incoming"])
    cmd = [cfg["youtubedl"], url]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)


def doYouTube(cfg, Q):
    try:
        while True:
            if Q.empty():
                time.sleep(1)
            else:
                iurl = Q.get()
                if iurl == "STOP":
                    Q.task_done()
                    break
                tmp = iurl.split("&")
                url = tmp[0]
                log.info(f"downloading {url}")
                getUrl(cfg, url)
                Q.task_done()
                log.info(f"{Q.qsize()} items on the Queue.")
    except Exception as e:
        log.error(f"Exception in doYouTube: {e}")
        sys.exit(1)


def main():
    """youtube urls look like

    https://www.youtube.com/watch?v=hMk6rF4Tzsg
    https://www.youtube.com/watch?v=pL3Yzjk5R4M&list=RDCMUCmM3eCpmWKLJj2PDW_jdGkg&start_radio=1&t=8

    config file at ~/.config/ytcb:
        ---
        incoming: /home/chris/Videos/kmedia/incoming
        youtubedl: /home/chris/bin/youtube-dl

    incoming is the path to store incoming videos from youtube
    youtubedl is the full path to the youtube-dl executable
    """
    log.info(f"{appname} - youtube-dl clipboard queue processor {ccacb.__version__}")
    userd = os.environ.get("HOME", os.path.expanduser("~"))
    defd = {
        "incoming": "/".join([userd]),
        "youtubedl": "/".join([userd, "bin/youtube-dl"]),
    }
    cf = ccaConfig(appname=appname, defaultd=defd)
    cfg = cf.envOverride()
    log.info(f"""Using {cfg["youtubedl"]}""")
    log.info(f"""youtube-dl will store files in {cfg["incoming"]}""")
    Q = queue.Queue()
    thread = threading.Thread(target=doYouTube, args=[cfg, Q])
    thread.start()
    try:
        while True:
            txt = waitForNewPaste()
            if txt.startswith("https://www.youtube.com/watch"):
                log.info(f"adding to Q: {txt}")
                Q.put(txt)
    except KeyboardInterrupt:
        log.info("Interrupted: Will finish off the Q, then exit")
    Q.put("STOP")
    thread.join()
    log.info(f"{appname} has finished")


if __name__ == "__main__":
    main()
