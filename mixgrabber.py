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


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc != 2:
        print(usage)
        exit()

    mixcloud_url = sys.argv[1]

    # get track web page and extract metadata
    print('Loading track page..')
    mixcloud_track = MixcloudTrack(mixcloud_url)

    mix_name = mixcloud_track.name

    # create directory for track and playlist
    if os.path.exists(mix_name):
        shutil.rmtree(mix_name)
    os.mkdir(mix_name)
    os.chdir(mix_name)

    # download track
    track_link = mixcloud_track.download_link
    track_name = mix_name + os.path.splitext(track_link)[1]

    downloader = Downloader()
    downloader.save_as(track_link, track_name)

    # create and save playlist
    cue_metadata = CueMetadataFile(mixcloud_track.name, mixcloud_track.owner, mixcloud_track.tracklist)
    cue_metadata.save()
