''' config for app '''


DB_NAME = 'tp_db'
DB_USER = 'tp_user'
DB_PASSWORD = 'tp123321'
DB_TABLE_PREFIX = 'testdrape2_'

LIBCDN = 'http://libs.baidu.com'

CACHE_HOST = '127.0.0.1'
CACHE_PORT = '11211'
CACHE_EXPIRE_TIME = 30 * 24 * 3600  # 30 days
SESSION_STORE_ENGINE = 'memcache'
# SESSION_STORE_ENGINE = 'file'
SESSION_MEMCACHE_CONNECTIONS = ['%s:%s' % (CACHE_HOST, CACHE_PORT)]

COFFEE_IS_DEBUG = False

AUTOLOGIN_DAY_LENGTH = 7

FONT_FILE_PATH = '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono.ttf'

TAG_RANDOM_RANGE_LENGTH = 100

MARKDOWN_DIR = 'frontend/markdown'
TEMPLATE_DIR = 'data/compiled/html'
