import os,sys
app_root = os.path.dirname(__file__)
os.chdir(app_root)
sys.path.append(app_root)

from drape.application import WsgiApplication
application = WsgiApplication()
