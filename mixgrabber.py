#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Vital Kolas'
__version__ = '0.4.1'
__date__ = '2014-03-04'

usage = """Usage:
- navigate to target directory
- run script
    mixgrabber.py http://link-to-mix-at-mixcloud.com

Ex.:
    cd music
    mixgrabber.py http://www.mixcloud.com/vplusplus/drifting-mind/"""

import os
from shutil import rmtree
from sys import argv
from threading import Thread
from urllib import request

from mixgrab.cue import CueFile
from mixgrab.mixcloud import MixcloudTrack
from mixgrab.downloader import Downloader


def get_content_length(content_url):
    r = request.urlopen(content_url)
    meta = r.info()
    meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
    meta_length = meta_func("Content-Length")
    file_size = int(meta_length[0]) if meta_length else 0
    return file_size

if __name__ == '__main__':
    if len(argv) != 2:
        print(usage)
        exit()

    mixcloud_url = argv[1]

    # get track web page and extract metadata
    print('Loading track page..')
    track = MixcloudTrack(mixcloud_url)

    track_name = track.name

    # create directory for track and playlist
    if os.path.exists(track_name):
        for root, dirs, files in os.walk(track_name):
            for file in files:
                os.unlink(os.path.join(root, file))
            for directory in dirs:
                rmtree(os.path.join(root, directory))
    else:
        os.mkdir(track_name)
    os.chdir(track_name)

    # prepare download params
    track_file_name = track_name + '.mp3'
    url = track.download_url
    track_size = get_content_length(url)
    thread_count = 100 if track_size else 1
    thread_size = track_size // thread_count

    with open(track_file_name, 'wb') as track_file:
        dl = Downloader(url, track_file)
        threads = []
        for i in range(thread_count):
            threads.append(Thread(
                target=dl.save_as,
                args=(i * thread_size, thread_size + (0 if i < thread_count - 1 else track_size % thread_size))
            ))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

    print('Finished')

    # create and save playlist
    CueFile(track.name, track.owner, track.tracklist).save()
