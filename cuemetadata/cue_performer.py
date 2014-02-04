__author__ = 'Vital Kolas'


class CuePerformer:
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
