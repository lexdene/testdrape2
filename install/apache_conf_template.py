import os


DOCUMENT_ROOT = '/home/elephant/workspace/webpage'
ROOT_URL = '/python/testdrape2'
ROOT_PATH = os.path.join(DOCUMENT_ROOT, ROOT_URL[1:])

TEMPLATE = '''DocumentRoot {DOCUMENT_ROOT}/
<Directory {DOCUMENT_ROOT}/>
  Options Indexes FollowSymLinks
  AllowOverride None
  Require all granted
</Directory>

Alias {ROOT_URL}/static/image/ {ROOT_PATH}/static/image/
Alias {ROOT_URL}/static/svg/ {ROOT_PATH}/static/svg/
Alias {ROOT_URL}/static/ {ROOT_PATH}/data/compiled/

WSGIScriptAlias {ROOT_URL}/ {ROOT_PATH}/wsgi-index.py/'''

print(TEMPLATE.format(
    DOCUMENT_ROOT=DOCUMENT_ROOT,
    ROOT_URL=ROOT_URL,
    ROOT_PATH=ROOT_PATH
))
