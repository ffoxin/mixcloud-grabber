__author__ = 'Vital Kolas'


class Cue:
    def print(self):
        pass


class CueOffset(Cue):
    def __init__(self, start):
        """
        :type start: int
        :param start: track offset, in seconds
        """
        self.start = start

    def print(self):
        """
        :rtype: str
        :return: track offset in cue format
        """
        m, s = divmod(self.start, 60)
        result = 'INDEX 01 {mm:02}:{ss:02}:00'.format(mm=m, ss=s)
        return result


class CuePerformer(Cue):
    def __init__(self, performer):
        """
        :type performer: str
        :param performer: performer (artist) name
        """
        self.performer = performer

    def print(self):
        """
        :rtype: str
        :return: performer (artist) name in cue format
        """
        result = 'PERFORMER "{performer}"'.format(performer=self.performer)
        return result


class CueTitle(Cue):
    def __init__(self, title):
        """
        :type title: str
        :param title: track name
        """
        self.title = title

    def print(self):
        """
        :rtype: str
        :return: track name in cue format
        """
        result = 'TITLE "{title}"'.format(title=self.title)
        return result


class CueTrack(Cue):
    def __init__(self, track):
        """
        :type track: (int, str, str, int)
        :param track: track metadata - index, title, performer, offset
        """
        self.index = track[0]
        self.title = CueTitle(track[1])
        self.performer = CuePerformer(track[2])
        self.offset = CueOffset(track[3])

    def print(self):
        """
        :rtype: str
        :return: separate track metadata in cue format
        """
        item = '    {}\n'

        result = '  TRACK {index} AUDIO\n'.format(index=self.index)
        result += item.format(self.title.print())
        result += item.format(self.performer.print())
        result += item.format(self.offset.print())

        return result


class CueTracklist(Cue):
    def __init__(self, tracklist):
        """
        :type tracklist: list[(int, str, str, int)]
        """
        self.tracklist = [CueTrack(track) for track in tracklist]

    def print(self):
        """
        :rtype: str
        :return: list of tracks in cue format
        """
        return ''.join(track.print() for track in self.tracklist)


class CueFile(Cue):
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
        :rtype: str
        :result: playlist in cue format
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
