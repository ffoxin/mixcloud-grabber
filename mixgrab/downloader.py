import multiprocessing
import sys
from urllib import request

parts_finished = 0


class Downloader:
    def __init__(self, url, file, dl_block_size=0x10000):
        """
        :type url: str
        :param url: file url to be downloaded
        :type dl_block_size: int
        :param dl_block_size: block size while downloading file
        """
        self.block_size = dl_block_size
        self.url = url
        self.file = file
        self.file_lock = multiprocessing.Lock()

    def save_as(self, save_offset=0, save_size=sys.maxsize):
        """
        :type save_offset: int
        :param save_offset: file offset to save downloaded data
        :type save_size: int
        :param save_size: file size to be downloaded
        """
        r = request.Request(self.url)
        r.headers['Range'] = 'bytes={}-'.format(save_offset)
        url_meta = request.urlopen(r)

        # save file
        downloaded = 0
        while downloaded != save_size:
            buffer = url_meta.read(self.block_size)
            if not buffer:  # if size not specified - continue until the end of file
                break

            with self.file_lock:
                self.file.seek(save_offset + downloaded)
                if downloaded + len(buffer) > save_size:
                    part = save_size - downloaded
                    self.file.write(buffer[:part])
                    break
                else:
                    self.file.write(buffer)
                    downloaded += len(buffer)

        url_meta.close()
        global parts_finished
        parts_finished += 1
        print('download finished {} bytes at {} offset [{}]'.format(save_size, save_offset, parts_finished))
