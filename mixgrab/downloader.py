from urllib import request
import threading
from socket import timeout

parts_finished = 0
tasks_completed = 0
tasks_count_lock = threading.Lock()
file_lock = threading.Lock()


class DownloadWorker(threading.Thread):
    def __init__(self, tasks_total, task_size, url, file):
        threading.Thread.__init__(self)
        self.tasks_total = tasks_total
        self.task_size = task_size
        self.url = url
        self.file = file
        self.current_task = -1

    def run(self):
        while True:
            with tasks_count_lock:
                global tasks_completed
                if self.tasks_total == tasks_completed:
                    break
                self.current_task = tasks_completed
                tasks_completed += 1

            self.save_as(self.current_task * self.task_size)

    def save_as(self, save_offset=0, dl_block_size=0x8000):
        r = request.Request(self.url)
        r.headers['Range'] = 'bytes={}-'.format(save_offset)

        while True:
            url_meta = request.urlopen(r, timeout=10)

            # save file
            downloaded = 0
            try:
                while downloaded != self.task_size:
                    buffer = url_meta.read(dl_block_size)
                    if not buffer:  # if size not specified - continue until the end of file
                        break

                    with file_lock:
                        self.file.seek(save_offset + downloaded)
                        if downloaded + len(buffer) > self.task_size:
                            part = self.task_size - downloaded
                            self.file.write(buffer[:part])
                            break
                        else:
                            self.file.write(buffer)
                            downloaded += len(buffer)
                url_meta.close()
                break
            except timeout:
                print('download task {} timeout. restarting'.format(self.current_task))
                url_meta.close()
                continue

        global parts_finished
        parts_finished += 1
        print('download task {} finished {} bytes at {} offset [{}]'.format(
            self.current_task, self.task_size, save_offset, parts_finished)
        )
