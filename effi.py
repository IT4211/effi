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
    _image.tsk(imgfile)

