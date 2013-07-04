__author__ = 'Vital Kolas'
__version__ = '0.1'
__date__ = '2013-07-04'

import re
import urllib.request

def get_download_link(track_link, max_servers):
    try:
        with urllib.request.urlopen(track_url) as url:
            track_page_data = url.read()
    except urllib.error.URLError:
        print('Error while opening track url.')
        return

    try:
        track_page = track_page_data.decode('utf-8', 'strict')
    except UnicodeError:
        print('Error while parsing track page.')
        return

    preview_url = re.search('(?<=\.mixcloud\.com/previews/)[^\.]+\.mp3', track_page)
    if preview_url is None:
        print('Preview link to *.mp3 not found.')
        return

    track_id = preview_url.group(0)
    download_template = 'http://stream{0}.mixcloud.com/cloudcasts/originals/' + track_id

    for i in range(1, max_servers):
        download_link = download_template.format(i)
        try:
            with urllib.request.urlopen(download_link) as url:
                return download_link
        except urllib.error.URLError:
            pass

    return

track_url = 'http://www.mixcloud.com/vplusplus/drifting-mind/'

print(get_download_link(track_url, 20))
