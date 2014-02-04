__author__ = 'Vital Kolas'


class CueOffset:
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
