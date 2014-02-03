import os
import sys
from urllib import request, parse


class Downloader:
    def __init__(self, dl_block_size=0x10000):
        """
        :type dl_block_size: int
        :param dl_block_size: block size while downloading file
        """
        self.block_size = dl_block_size

    def save_as(self, url, file_name=None, size=sys.maxsize):
        """
        :type url: str
        :param url: file url to be downloaded
        :type file_name: str
        :param file_name: file name to be saved as
        :type size: int
        :param size: file size to be downloaded
        """
        url_meta = request.urlopen(url)
        url_real = url_meta.geturl()

        # get file name
        scheme, netloc, path, query, fragment = parse.urlsplit(url_real)
        if not file_name:
            file_name = os.path.basename(path)
        if not file_name:
            file_name = 'mixcloud_track.mp3'

        # save file
        with open(file_name, 'wb') as dl_file:
            downloaded = 0
            '''while True:
                buffer = url_meta.read(self.block_size)
                if not buffer:
                    break

                if downloaded + len(buffer) > size:
                    part = size - downloaded
                    dl_file.write(buffer[:part])
                    break
                else:
                    downloaded += len(buffer)
                    dl_file.write(buffer)'''
            print('{} - download finished'.format(file_name))

        return file_name
