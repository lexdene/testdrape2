import time

import drape.debug as debug
import drape.config

def init(a):
    # update app config
    import app.config.config as appconfig
    drape.config.include(appconfig)

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
    debug.debug("uri: %s"%request.REQUEST_URI)
    debug.debug("urlpath: %s"%request.urlPath())
    debug.debug("ip: %s"%request.REMOTE_ADDR)
    debug.debug("refer: %s"%request.HTTP_REFERER)
    debug.debug("user agent: %s"%request.HTTP_USER_AGENT)

def run_begin(runbox):
    debug.debug('  ====  RUN BEGIN ====  ')
    runbox.variables()['run_begin_time'] = time.time()

def run_end(runbox):
    run_begin_time = runbox.variables().get('run_begin_time')
    run_end_time = time.time()
    debug.debug('runtime: %f'%(run_end_time-run_begin_time))
