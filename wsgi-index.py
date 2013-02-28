import os,sys
app_root = os.path.dirname(__file__)
os.chdir(app_root)
sys.path.append(app_root)

import drape

application = drape.application.WsgiApplication()
application.start()
