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
    ),
    'app': dict(
        autologin_daylength=7,
    )
}
