<<<<<<< HEAD
#-*- coding: utf-8 -*-
import ConfigParser # conf file parsing

def extractconf():

    config = ConfigParser.ConfigParser()
    config.read('option.cfg')
    if config.has_section('extract_option'):
        options = config.items('extract_option')
        # TODO : 옵션이 적절한 형태로 지정됬을 때 부분 검사 .get method 알아보기

    return options

=======
#-*- coding: utf-8 -*-
import ConfigParser # conf file parsing

def extractconf():

    config = ConfigParser.ConfigParser()
    config.read('option.cfg')
    if config.has_section('extract_option'):
        options = config.items('extract_option')
        # TODO : 옵션이 적절한 형태로 지정됬을 때 부분 검사 .get method 알아보기

    return options
>>>>>>> dd1f28e1f3eaa842c3060e046b614daadf029f30
