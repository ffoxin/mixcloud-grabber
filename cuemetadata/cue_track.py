__author__ = 'Vital Kolas'


class CueTrack:
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
