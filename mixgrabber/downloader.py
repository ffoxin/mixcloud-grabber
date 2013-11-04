import os
import math
from urllib import request, parse


class Downloader:
    def __init__(self, dl_block_size=0xFFFF):
        """
        @type dl_block_size: int
        @param dl_block_size: block size while downloading file
        """
        self.block_size = dl_block_size

    def save_as(self, url, file_name=None):
        """
        @type url: str
        @param url: file url to be downloaded
        @type file_name: str
        @param file_name: file name to be saved as
        """
        url_meta = request.urlopen(url)
        url_real = url_meta.geturl()

        scheme, netloc, path, query, fragment = parse.urlsplit(url_real)
        if not file_name:
            file_name = os.path.basename(path)
        if not file_name:
            file_name = 'mixcloud_track.mp3'

        with open(file_name, 'wb') as dl_file:
            meta = url_meta.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func("Content-Length")
            file_size = int(meta_length[0]) if meta_length else 0
            print("Downloading: {0} Bytes: {1}".format(file_name, file_size))

            downloaded = 0
            size_length = int(math.log10(file_size)) + 1
            while True:
                buffer = url_meta.read(self.block_size)
                if not buffer:
                    break

                downloaded += len(buffer)
                dl_file.write(buffer)

                status = repr(downloaded).rjust(size_length)
                if file_size:
                    status += " [{0:.2f}%]".format(downloaded * 100 / file_size)
                status += chr(13)
                print(status, end="")
            print()

        return file_name
