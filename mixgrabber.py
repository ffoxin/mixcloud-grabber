__author__ = 'Vital Kolas'
__version__ = '0.3.0'
__date__ = '2013-11-04'

import os
import shutil
from mixgrabber.cuemeta import CueMetadataFile
from mixgrabber.mixcloud import MixcloudTrack
from mixgrabber.downloader import Downloader


if __name__ == '__main__':
    mixcloud_url = 'http://www.mixcloud.com/spookybizzle/spookys-short-n-sweet-uk-garage-mix/'

    # get track web page and extract metadata
    mixcloud_track = MixcloudTrack(mixcloud_url)

    # create directory for track and playlist
    mix_name = mixcloud_track.name
    if os.path.exists(mix_name):
        shutil.rmtree(mix_name)
    os.mkdir(mix_name)
    os.chdir(mix_name)

    # download track
    track_link = mixcloud_track.download_link
    track_name = mix_name + os.path.splitext(track_link)[1]

    downloader = Downloader()
    downloader.save_as(track_link, track_name)

    cue_metadata = CueMetadataFile(mixcloud_track.name, mixcloud_track.owner, mixcloud_track.tracklist)
    cue_metadata.save()
