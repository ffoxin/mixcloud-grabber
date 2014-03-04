import json
import re
from urllib import error, request
from xml.etree import ElementTree


class MixcloudTrack:
    def __init__(self, url, server_count=30):
        """
        :type url: str
        :param url: link to track at mixcloud.com
        :type server_count: int
        :param server_count: maximum server index
        """
        self.download_url = ''
        self.name = ''
        self.owner = ''
        self.tracklist = None

        self.track_url = url
        self.meta_url = url.replace('http://www.mixcloud.com/', 'http://api.mixcloud.com/', 1)
        self.get_download_link(server_count)
        self.load_playlist_info()

    def page(self):
        """
        :rtype: str
        :return: html page
        """
        with request.urlopen(self.track_url) as track_url:
            data = track_url.read()
        data_string = data.decode('utf-8', 'strict')
        return data_string

    def id(self):
        """
        :rtype: str
        :return: track id
        """
        track_id = ''

        preview_url = re.search('(?<=\.mixcloud\.com/previews/)([^\.]+\.)(?=mp3)', self.page())
        if preview_url:
            track_id = preview_url.group(0)

        return track_id

    def get_download_link(self, server_count):
        """
        :type server_count: number
        :param server_count: maximum number of servers to be checked
        :rtype: str
        :return: direct link to mp3 file
        """

        track_id = self.id()
        if track_id.startswith('7/f/2/7'):
            download_template = 'http://stream{0}.mixcloud.com/c/m4a/64/' + track_id + 'm4a'
        elif track_id.startswith('6/c/1/f'):
            download_template = 'http://stream{0}.mixcloud.com/c/originals/' + track_id + 'mp3'
        else:
            print('Unknown id format; try use default')
            download_template = 'http://stream{0}.mixcloud.com/c/m4a/64/' + track_id + 'm4a'

        download_link = ''
        for i in range(server_count):
            download_link = download_template.format(i)
            try:
                request.urlopen(download_link)
            except error.URLError:
                pass
            else:
                break

        self.download_url = download_link

    def load_playlist_info(self):
        """
        :rtype: list
        :return: list of (track, artist) pairs
        """
        with request.urlopen(self.meta_url) as meta_url:
            meta_data = meta_url.read()
            meta_json = meta_data.decode('utf-8', 'strict')
            meta = json.loads(meta_json)

        self.name = meta['name']
        self.owner = meta['user']['username']

        self.tracklist = [
            (section['position'],
             section['track']['artist']['name'],
             section['track']['name'],
             # 2014-04-03 there is a bug on mixcloud service
             # missed 'start_time' parameter within mp3 mixes
             section['start_time'] if 'start_time' in section else 0)
            for section
            in meta['sections']
        ]
