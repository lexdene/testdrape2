from drape.router import Resource, Group, Url
from drape.request import GET, POST

routes = [
    Url(
        '^/$',
        GET,
        'index.index'
    ),
    Url(
        '^/db/create_tables$',
        GET,
        'db.create_tables'
    ),
    Url(
        '^/user/Login$',
        GET,
        'user.Login'
    ),
    Url(
        '^/user/ajaxRegister$',
        POST,
        'user.ajaxRegister'
    ),
    Url(
        '^/common/validate_code_image$',
        GET,
        'common.validate_code_image'
    ),
]
