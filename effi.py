<<<<<<< HEAD
#-*- coding: utf-8 -*-
"""
@Author : SeonHo Lee (IT4211)
@Email  : rhdqor100@live.co.kr
@Description : Extract a file from an image file
"""

import _effi
import _image

if __name__=='__main__':

    imgfile = _effi.ParseCommandLine()
    effi = _image.tsk(imgfile)
    effi.loadimage()
    effi.setconf()
    #effi.extractfile()
    dir = effi.open_directory('/Windows')
    effi.list_directory(dir, [])
    #effi.debug_print_extlist()
    effi.extract_directory_entry()

=======
#-*- coding: utf-8 -*-
"""
@Author : SeonHo Lee (IT4211)
@Email  : rhdqor100@live.co.kr
@Description : Extract a file from an image file
"""

import _effi
import _image

if __name__=='__main__':

    imgfile = _effi.ParseCommandLine()
    effi = _image.tsk(imgfile)
    effi.loadimage()
    effi.setconf()
    #effi.extractfile()
    dir = effi.open_directory('/Windows')
    effi.list_directory(dir, [])
    #effi.debug_print_extlist()
    #effi.extract_directory_entry()

>>>>>>> dd1f28e1f3eaa842c3060e046b614daadf029f30
