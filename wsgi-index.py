import os, sys
app_root = os.path.dirname(__file__)
sys.path.append(app_root)

from drape.application import WsgiApplication
import app


application = WsgiApplication(
    root_dir=app_root
)
