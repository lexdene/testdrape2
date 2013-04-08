import drape.debug as debug

def init(a):
    eventCenter = a.eventCenter()
    eventCenter.registerHandler(
        'after_request_run',
        after_request_run
    )

def after_request_run(application,request):
    debug.debug(request.HTTP_USER_AGENT)
    debug.debug("uri:%s urlpath:%s ip:%s refer:%s"%(
        request.REQUEST_URI,
        request.urlPath(),
        request.REMOTE_ADDR,
        request.HTTP_REFERER,
        #request.userAgent()
    ))
			
