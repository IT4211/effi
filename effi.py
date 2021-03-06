#-*- coding: utf-8 -*-
"""
@Author : SeonHo Lee (IT4211)
@Email  : rhdqor100@live.co.kr
@Description : Extract a file from an image file
"""

import _effi
import _image

if __name__=='__main__':

    imgfile, path_option = _effi.ParseCommandLine()
    effi = _image.tsk(imgfile)
    effi.loadimage()
    effi.setconf()
    #effi.extractfile()
    dir = effi.open_directory('/')
    effi.list_directory(dir, [], [])
    #effi.debug_print_extlist()
    effi.extract_directory_entry(path_option)
