__author__ = 'Vital Kolas'


class CueTitle:
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
