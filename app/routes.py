'define routes'
from drape.router import (
    Group,
    Url,
    Resource,
    define_routes,
    define_controller
)
from . import controller


define_controller(controller)

define_routes(
    Url.get('', 'index.index'),
    Group(
        'db',
        Url.get('create_tables'),
    ),
    Group(
        'user',
        Url.get('Register'),
        Url.post('ajaxRegister'),
        Url.get('Login'),
        Url.post('ajaxLogin'),
        Url.get('Logout'),
    ),
    Group(
        'common',
        Url.get('validate_code_image')
    ),
    Group(
        'discuss',
        Resource(
            'topic',
            members=[
                Resource('reply')
            ]
        )
    ),
    Resource(
        'notice'
    ),
    Resource(
        'userinfo',
        members=[
            Resource('action'),
            Resource('message'),
        ],
    ),
    Resource('focus'),
    Url.get('home', 'home.index'),
)
