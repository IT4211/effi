import ConfigParser # conf file parsing

def extractconf():

    config = ConfigParser.ConfigParser()
    config.read('option.cfg')
    if config.has_section('extract_option'):
        options = config.items('extract_option')
        # TODO : 옵션이 적절한 형태로 지정됬을 때 부분 검사 .get method 알아보기

    return options