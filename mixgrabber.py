#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Vital Kolas'
__version__ = '0.3.2'
__date__ = '2013-11-04'

usage = """Usage:
- navigate to target directory
- run script
    mixgrabber.py http://link-to-mix-at-mixcloud.com

Ex.:
    cd music
    mixgrabber.py http://www.mixcloud.com/vplusplus/drifting-mind/"""

import os
import shutil
import sys

from mixgrabber.cuemeta import CueMetadataFile
from mixgrabber.mixcloud import MixcloudTrack
from mixgrabber.downloader import Downloader

import threading


def get_content_length(url):
    r = request.urlopen(url)

    meta = r.info()
    meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
    meta_length = meta_func("Content-Length")
    file_size = int(meta_length[0]) if meta_length else 0
    return file_size

from urllib import request

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(usage)
        exit()

    mixcloud_url = sys.argv[1]

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
                shutil.rmtree(os.path.join(root, directory))
    else:
        os.mkdir(track_name)
    os.chdir(track_name)

    track_file = track_name + '.mp3'

    url = track.download_link + '?start='
    full_size = get_content_length(url + '0')
    thread_count = 100
    length = track.length
    length_part = length // thread_count
    stamps = [get_content_length(url + str(length_part * i)) for i in range(thread_count)]
    stamps.append(0)
    lengths = [stamps[i] - stamps[i + 1] for i in range(thread_count)]
    print(stamps)
    print(lengths)

    dl = Downloader()
    trs = []
    for i in range(thread_count):
        url_i = url + str(length_part * i)
        file_i = track_file + '.part{:02}'.format(i)
        trs.append(threading.Thread(
            target=dl.save_as,
            args=(url_i, file_i, lengths[i])
        ))

    for tr in trs:
        tr.start()

    for tr in trs:
        tr.join()

    print('Finished')

    # create and save playlist
    CueMetadataFile(track.name, track.owner, track.tracklist).save()
