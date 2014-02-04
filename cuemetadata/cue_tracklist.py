__author__ = 'Vital Kolas'


class CueTracklist:
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
