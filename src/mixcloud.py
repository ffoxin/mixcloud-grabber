__author__ = 'Vital Kolas'
__version__ = '0.2.1'
__date__ = '2013-07-04'

import re
from urllib import request, error, parse
import os


class CueMetadataIndex:
    def __init__(self, start):
        """
        @type start: str
        @param start: track offset from beginning, in seconds
        """

        self.start = int(start)

    def print(self):
        """
        @rtype: str
        @return: track offset in cue format
        """
        m, s = divmod(self.start, 60)
        result = 'INDEX 01 {mm:02}:{ss:02}:00'.format(mm=m, ss=s)
        return result


class CueMetadataTitle:
    def __init__(self, title):
        """
        @type title: str
        @param title: track name
        """
        self.title = title

    def print(self):
        """
        @rtype: str
        @return: track name in cue format
        """
        result = 'TITLE "{}"'.format(self.title)
        return result


class CueMetadataPerformer:
    def __init__(self, performer):
        """
        @type performer: str
        @param performer: artist name
        """
        self.performer = performer

    def print(self):
        """
        @rtype: str
        @return: artist name in cue format
        """
        result = 'PERFORMER "{}"'.format(self.performer)
        return result


class CueMetadataTrack:
    def __init__(self, order_number, title, performer, index):
        """
        @type order_number: int
        @param order_number: track number in file
        @type title: str
        @param title: track name
        @type performer: str
        @param performer: artist name
        @type index: str
        @param index: track offset from beginning, in seconds
        """
        self.order_number = order_number
        self.title = CueMetadataTitle(title)
        self.performer = CueMetadataPerformer(performer)
        self.index = CueMetadataIndex(index)

    def print(self):
        """
        @rtype: str
        @return: separate track metadata in cue format
        """
        item = '    {}\n'

        result = '  TRACK {}.mp3 AUDIO\n'.format(self.order_number)
        result += item.format(self.title.print())
        result += item.format(self.performer.print())
        result += item.format(self.index.print())

        return result


class CueMetadataTracklist:
    def __init__(self, tracklist):
        """
        @type tracklist: []
        """
        self.tracklist = []
        n = 0
        for track in tracklist:
            n += 1
            self.tracklist.append(CueMetadataTrack(n, track[0], track[1], track[2]))

    def print(self):
        """
        @rtype: str
        @return: list of tracks in cue format
        """
        result = ''
        for track in self.tracklist:
            result += track.print()

        return result


class CueMetadataFile:
    def __init__(self, file, title, performer, tracklist):
        """
        @type file: str
        @param file: file name (without extension)
        @type title: str
        @param title: tracklist name
        @type performer: str
        @param performer: tracklist owner
        @type tracklist: zip
        @param tracklist: tracks' metadata
        """
        self.file = file
        self.title = CueMetadataTitle(title)
        self.performer = CueMetadataPerformer(performer)
        self.tracklist = CueMetadataTracklist(tracklist)

    def print(self):
        """
        @rtype: str
        @result: playlist in cue format
        """
        line = '{}\n'
        result = 'FILE "{}" MP3\n'.format(self.file)
        result += line.format(self.title.print())
        result += line.format(self.performer.print())
        result += self.tracklist.print()

        return result


class MixcloudTrack:
    def __init__(self, track_url):
        """
        @type track_url: str
        @param track_url: link to track at mixcloud.com
        """
        self.download_link = ''
        self.name = ''
        self.owner = ''
        self.tracklist = None

        self.url = track_url
        self.get_download_link(30)
        self.load_playlist_info()

    def page(self):
        """
        @rtype: str
        @return: html page
        """
        with request.urlopen(self.url) as track_url:
            data = track_url.read()
        data_string = data.decode('utf-8', 'strict')
        return data_string

    def id(self):
        """
        @rtype: str
        @return: track id
        """
        track_id = ''
        preview_url = re.search('(?<=\.mixcloud\.com/previews/)[^\.]+\.mp3', self.page())
        if preview_url:
            track_id = preview_url.group(0)

        return track_id

    def get_download_link(self, server_count):
        """
        @type server_count: number
        @param server_count: maximum number of servers to be checked
        @rtype: str
        @return: direct link to mp3 file
        """
        download_template = 'http://stream{0}.mixcloud.com/cloudcasts/originals/' + self.id()

        download_link = ''
        for i in range(server_count):
            download_link = download_template.format(i)
            try:
                request.urlopen(download_link)
            except error.URLError:
                pass
            else:
                break

        self.download_link = download_link

    def load_playlist_info(self):
        page = self.page()

        self.name = re.search('<h1[^>]*?cloudcast-name[^>]*>([^<]+)<', page).group(1)
        self.owner = re.search('<a[^>]*?cloudcast-owner-link[^>]*><span itemprop="name">([^<]+)<', page).group(1)

        titles = re.findall('(?<=class="tracklisttrackname mx-link">)[^<]*', page)
        artists = re.findall('(?<=class="tracklistartistname mx-link">)[^<]*', page)
        durations = re.findall('(?<=data-sectionstart=")\d+(?=">)', page)

        self.tracklist = zip(titles, artists, durations)


def download_file(file_url, desc=None):
    u = request.urlopen(file_url)

    scheme, netloc, path, query, fragment = parse.urlsplit(file_url)
    file_name = os.path.basename(path)
    if not file_name:
        file_name = 'downloaded.file'
    if desc:
        file_name = os.path.join(desc, file_name)

    with open(file_name, 'wb') as f:
        meta = u.info()
        meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
        meta_length = meta_func("Content-Length")
        file_size = None
        if meta_length:
            file_size = int(meta_length[0])
        print("Downloading: {0} Bytes: {1}".format(file_url, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            status = "{0:16}".format(file_size_dl)
            if file_size:
                status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
            status += chr(13)
            print(status, end="")
        print()

    return file_name

if __name__ == '__main__':

    #track_url = 'http://www.mixcloud.com/vplusplus/drifting-mind/'
    #track = MixcloudTrack(track_url)

    #cue = CueMetadataFile(track.name.replace(' ', '_'), track.name, track.owner, track.tracklist)

    #print('Download link:\n{}\n'.format(track.downloadLink))
    #print('Save as...\n{}\n'.format(cue.file + '.mp3'))
    #print('Cue file:\n{}\n\n{}\n'.format(cue.file + '.cue', cue.print()))


    url = "http://download.thinkbroadband.com/10MB.zip"
    filename = download_file(url)
    print(filename)