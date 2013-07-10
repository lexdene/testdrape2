''' config for app '''

CONFIG = {
    'db': dict(
        user='tp_user',
        password='tp123321',
        dbname='tp_db',
        tablePrefix='testdrape2_',
    ),
    'sae_storage': dict(
        domain_name='storage'
    ),
    'system': dict(
        font_path='/usr/share/fonts/truetype/ttf-dejavu/DejaVuSansMono.ttf',
        libcdn='http://libs.baidu.com'
    ),
    'app': dict(
        autologin_daylength=7,
    ),
    'front': dict(
        coffee_debug=False
    ),
    'tag': dict(
        random_range_length=20,
    )
}
