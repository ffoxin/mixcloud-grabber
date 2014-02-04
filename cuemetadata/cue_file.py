from cuemetadata.cue_title import CueTitle
from cuemetadata.cue_performer import CuePerformer
from cuemetadata.cue_tracklist import CueTracklist

__author__ = 'Vital Kolas'


class CueFile:
    def __init__(self, title, performer, tracklist):
        """
        :type title: str
        :param title: tracklist name
        :type performer: str
        :param performer: tracklist owner
        :type tracklist: list[(int, str, str, int)]
        :param tracklist: tracks' metadata
        """
        self.track_name = title
        self.title = CueTitle(title)
        self.performer = CuePerformer(performer)
        self.tracklist = CueTracklist(tracklist)

    def print(self):
        """
        @rtype: str
        @result: playlist in cue format
        """
        line = '{}\n'
        result = 'FILE "{track}.mp3" MP3\n'.format(track=self.track_name)
        result += line.format(self.title.print())
        result += line.format(self.performer.print())
        result += self.tracklist.print()

        return result

    def save(self):
        file_name = self.track_name + '.cue'

        with open(file_name, 'w') as cue_file:
            cue_file.write(self.print())

        print('Playlist "{}" created'.format(file_name))
