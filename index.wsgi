import os,sys
app_root = os.path.dirname(__file__)
os.chdir(app_root)
sys.path.append(app_root)

import drape
import sae

app = drape.SaeApplication()
app.start()

application = sae.create_wsgi_app(app)
