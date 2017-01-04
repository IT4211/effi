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
            filenames = pyewf.glob(self.url)
            ewf_handle = pyewf.handle()
            ewf_handle.open(filenames)
            img_info = ewf_Img_Info(ewf_handle)
            self.fs_info = pytsk3.FS_Info(img_info, offset=63 * 512)

        elif ext in rawformat:
            # TODO : pytsk
            img_info = pytsk3.Img_Info(url = self.url)
            self.fs_info = pytsk3.FS_Info(img_info)




    def setconf(self):
        # TODO : Extract condition from configuration file
        self.conf = _conf.extractconf()

    def extractfile(self):
        # TODO : Extract files with settings applied

class ewf_Img_Info(pytsk3.Img_info):
    def __init__(self, ewf_handle):
        self._ewf_handle = ewf_handle
        super(ewf_Img_Info, self).__init__(
            url="", type=pytsk3.TSK_IMG_TYPE_EXTERNAL)

    def close(self):
        self._ewf_handle.close()

    def read(self, offset, size):
        self._ewf_handle.seek(offset)
        return self._ewf_handle.read(size)

    def get_size(self):
        return self._ewf_handle.get_media_size()

