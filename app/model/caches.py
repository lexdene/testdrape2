'some cache by functions'
from drape.model import LinkedModel

from app.lib.cache import cache_by


@cache_by('userinfo/{0}')
def get_userinfo(uid):
    'userinfo by uid'
    return LinkedModel(
        'userinfo'
    ).where(
        id=uid
    ).find()


@cache_by('notice_count/{0}')
def get_notice_count(uid):
    'notice count by uid'
    return LinkedModel(
        'notice'
    ).where(
        to_uid=uid,
        isRead=0
    ).count()


@cache_by('mail_count/{0}')
def get_mail_count(uid):
    'mail count by uid'
    return LinkedModel(
        'mail'
    ).where(
        to_uid=uid,
        isRead=0
    ).count()
