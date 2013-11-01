class CueMetadataIndex:
    def __init__(self, start):
        """
        @type start: str
        @param start: track offset from beginning, in seconds
        """

        self.start = int(start)

    def print(self):
        """
        @rtype: str
        @return: track offset in cue format
        """
        m, s = divmod(self.start, 60)
        result = 'INDEX 01 {mm:02}:{ss:02}:00'.format(mm=m, ss=s)
        return result


class CueMetadataTitle:
    def __init__(self, title):
        """
        @type title: str
        @param title: track name
        """
        self.title = title

    def print(self):
        """
        @rtype: str
        @return: track name in cue format
        """
        result = 'TITLE "{}"'.format(self.title)
        return result


class CueMetadataPerformer:
    def __init__(self, performer):
        """
        @type performer: str
        @param performer: artist name
        """
        self.performer = performer

    def print(self):
        """
        @rtype: str
        @return: artist name in cue format
        """
        result = 'PERFORMER "{}"'.format(self.performer)
        return result


class CueMetadataTrack:
    def __init__(self, order_number, title, performer, index):
        """
        @type order_number: int
        @param order_number: track number in file
        @type title: str
        @param title: track name
        @type performer: str
        @param performer: artist name
        @type index: str
        @param index: track offset from beginning, in seconds
        """
        self.order_number = order_number
        self.title = CueMetadataTitle(title)
        self.performer = CueMetadataPerformer(performer)
        self.index = CueMetadataIndex(index)

    def print(self):
        """
        @rtype: str
        @return: separate track metadata in cue format
        """
        item = '    {}\n'

        result = '  TRACK {}.mp3 AUDIO\n'.format(self.order_number)
        result += item.format(self.title.print())
        result += item.format(self.performer.print())
        result += item.format(self.index.print())

        return result


class CueMetadataTracklist:
    def __init__(self, tracklist):
        """
        @type tracklist: []
        """
        self.tracklist = []
        n = 0
        for track in tracklist:
            n += 1
            self.tracklist.append(CueMetadataTrack(n, track[0], track[1], track[2]))

    def print(self):
        """
        @rtype: str
        @return: list of tracks in cue format
        """
        result = ''
        for track in self.tracklist:
            result += track.print()

        return result


class CueMetadataFile:
    def __init__(self, file, title, performer, tracklist):
        """
        @type file: str
        @param file: file name (without extension)
        @type title: str
        @param title: tracklist name
        @type performer: str
        @param performer: tracklist owner
        @type tracklist: zip
        @param tracklist: tracks' metadata
        """
        self.file = file
        self.title = CueMetadataTitle(title)
        self.performer = CueMetadataPerformer(performer)
        self.tracklist = CueMetadataTracklist(tracklist)

    def print(self):
        """
        @rtype: str
        @result: playlist in cue format
        """
        line = '{}\n'
        result = 'FILE "{}" MP3\n'.format(self.file)
        result += line.format(self.title.print())
        result += line.format(self.performer.print())
        result += self.tracklist.print()

        return result
