import re
from urllib import error, request


class MixcloudTrack:
    def __init__(self, url):
        """
        @type url: str
        @param url: link to track at mixcloud.com
        """
        self.download_link = ''
        self.name = ''
        self.owner = ''
        self.tracklist = None

        self.url = url
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
