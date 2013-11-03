__author__ = 'Vital Kolas'
__version__ = '0.3.0'
__date__ = '2013-11-01'

import os
from cuemeta import CueMetadataFile
from mixcloud import MixcloudTrack


if __name__ == '__main__':
    mixcloud_url = 'http://www.mixcloud.com/vplusplus/drifting-mind/'
    track = MixcloudTrack(mixcloud_url)

    cue = CueMetadataFile(track.name.replace(' ', '_'), track.name, track.owner, track.tracklist)

    link = track.download_link
    title = cue.file
    cue_name = '{}.cue'.format(title)
    track_name = '{name}{ext}'.format(name=title, ext=os.path.splitext(link)[1])
    print(title)
    print(cue_name)
    print(track_name)

    #print('Download link:\n{}\n'.format(track.download_link))
    #print('Save as...\n{}\n'.format(cue.file + '.mp3'))
    #print('Cue file:\n{}\n\n{}\n'.format(cue.file + '.cue', cue.print()))


    #url = "http://download.thinkbroadband.com/10MB.zip"
    #filename = download_file(url)
    #print(filename)