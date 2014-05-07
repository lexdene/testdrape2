from drape.router import Resource, Group, Url
from drape.request import GET

routes = [
    Url(
        '^/$',
        GET,
        'index.index'
    ),
    Url(
        '^/user/Login$',
        GET,
        'user.Login'
    ),
    Url(
        '^/common/validate_code_image$',
        GET,
        'common.validate_code_image'
    ),
]
