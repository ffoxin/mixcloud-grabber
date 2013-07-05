__author__ = 'Vital Kolas'
__version__ = '0.2'
__date__ = '2013-07-04'

import re
from urllib import request, error


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
    def __init__(self, orderNumber, title, performer, index):
        """
        @type orderNumber: int
        @param orderNumber: track number in file
        @type title: str
        @param title: track name
        @type performer: str
        @param performer: artist name
        @type index: str
        @param index: track offset from beginning, in seconds
        """
        self.orderNumber = orderNumber
        self.title = CueMetadataTitle(title)
        self.performer = CueMetadataPerformer(performer)
        self.index = CueMetadataIndex(index)

    def print(self):
        """
        @rtype: str
        @return: separate track metadata in cue format
        """
        item = '    {}\n'

        result = '  TRACK {}.mp3 AUDIO\n'.format(self.orderNumber)
        result += item.format(self.title.print())
        result += item.format(self.performer.print())
        result += item.format(self.index.print())

        return result


class CueMetadataTracklist:
    def __init__(self, trackList):
        """
        @type trackList: []
        """
        self.trackList = []
        n = 0
        for track in trackList:
            n += 1
            self.trackList.append(CueMetadataTrack(n, track[0], track[1], track[2]))

    def print(self):
        """
        @rtype: str
        @return: list of tracks in cue format
        """
        result = ''
        for track in self.trackList:
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
    def __init__(self, url):
        """
        @type url: str
        @param url: link to track at mixcloud.com
        """
        self.url = url
        self.getDownloadLink(30)
        self.loadPlaylistInfo()

    def page(self):
        """
        @rtype: str
        @return: html page
        """
        with request.urlopen(self.url) as url:
            data = url.read()
        sData = data.decode('utf-8', 'strict')
        return sData

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

    def getDownloadLink(self, nServers):
        """
        @type nServers: number
        @param nServers: maximum number of servers to be checked
        @rtype: str
        @return: direct link to mp3 file
        """
        download_template = 'http://stream{0}.mixcloud.com/cloudcasts/originals/' + self.id()

        downloadLink = ''
        for i in range(nServers):
            downloadLink = download_template.format(i)
            try:
                request.urlopen(downloadLink)
            except error.URLError:
                pass
            else:
                break

        self.downloadLink = downloadLink

    def loadPlaylistInfo(self):
        page = self.page()

        self.name = re.search('<h1[^>]*?cloudcast-name[^>]*>([^<]+)<', page).group(1)
        self.owner = re.search('<a[^>]*?cloudcast-owner-link[^>]*>([^<]+)<', page).group(1)

        titles = re.findall('(?<=class="tracklisttrackname mx-link">)[^<]*', page)
        artists = re.findall('(?<=class="tracklistartistname mx-link">)[^<]*', page)
        durations = re.findall('(?<=data-sectionstart=")\d+(?=">)', page)

        self.tracklist = zip(titles, artists, durations)


if __name__ == '__main__':
    track_url = 'http://www.mixcloud.com/vplusplus/bicycle-day-with-oblank/'
    track = MixcloudTrack(track_url)

    cue = CueMetadataFile(track.name.replace(' ', '_'), track.name, track.owner, track.tracklist)

    print('Download link:\n{}\n'.format(track.downloadLink))
    print('Save as...\n{}\n'.format(cue.file + '.mp3'))
    print('Cue file:\n{}\n\n{}\n'.format(cue.file + '.cue', cue.print()))
