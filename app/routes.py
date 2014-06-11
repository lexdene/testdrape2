'define routes'
from drape.router import Group, Url
from drape.request import GET

ROUTES = [
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
    Group(
        'user',
        Url.get('Register'),
        Url.post('ajaxRegister'),
        Url.get('Login'),
        Url.post('ajaxLogin'),
        Url.get('Logout'),
    ),
    Url(
        '^/common/validate_code_image$',
        GET,
        'common.validate_code_image'
    ),
]
