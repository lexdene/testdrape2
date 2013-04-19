import time

import drape.debug as debug

def init(a):
    eventCenter = a.eventCenter()
    eventCenter.registerHandler(
        'after_request_run',
        after_request_run
    )
    eventCenter.registerHandler(
        'run_begin',
        run_begin
    )
    eventCenter.registerHandler(
        'run_end',
        run_end
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
			
def run_begin(runbox):
    runbox.variables()['run_begin_time'] = time.time()

def run_end(runbox):
    run_begin_time = runbox.variables().get('run_begin_time')
    run_end_time = time.time()
    debug.debug('runtime: %f'%(run_end_time-run_begin_time))
