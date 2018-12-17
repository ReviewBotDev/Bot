for id, serv in BigWorld.localServices.items():
    if serv.__class__.__name__ == 'HttpRequester':
        INFO('Http request reset')
        serv._HttpRequester__cache.clear()