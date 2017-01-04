import pytsk3 # raw image analysis and file system analysis
import pyewf  # ewf iamge file processing
import os
import _conf

class tsk():

    def __init__(self, url):
        self.url = url

    def loadimage(self):
        ewformat = ['.s01', '.E01', '.Ex01']
        rawformat = ['.dd', '.raw']
        ext = os.path.splitext(self.url)
        if ext in ewformat:
            # TODO : pyewf
        elif ext in rawformat:
            # TODO : pytsk

    def configuration(self):
        # TODO : Extract condition from configuration file
        self.conf = _conf.extractconf()

    def extractfile(self):
        # TODO : Extract files with settings applied
