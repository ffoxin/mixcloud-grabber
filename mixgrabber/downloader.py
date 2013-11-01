import os
from urllib import request, parse


def download_file(file_url, file_name=None):
    u = request.urlopen(file_url)

    scheme, netloc, path, query, fragment = parse.urlsplit(file_url)
    if not file_name:
        file_name = os.path.basename(path)
    if not file_name:
        file_name = 'downloaded.file'

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