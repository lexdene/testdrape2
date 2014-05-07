import os,sys
app_root = os.path.dirname(__file__)
os.chdir(app_root)
sys.path.append(app_root)
sys.path.append(
    os.path.normpath(
        os.path.join(
            app_root,
            '../../../python'
        )
    )
)

from drape.application import WsgiApplication
application = WsgiApplication()
