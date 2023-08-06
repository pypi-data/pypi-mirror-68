from .utils import resolveUser
from ..mixins import BaseApp


class SentryToken(BaseApp):
    _attrTypes = {**BaseApp._attrTypes, 'dsn': 'str'}
    _editableAttrs = BaseApp._editableAttrs + ['dsn']
    _path = '/sentry_tokens'
    _credmgrCallable = 'sentryToken'

    def __init__(self, credmgr, id=None, appName=None, dsn=None, enabled=None, ownerId=None):
        super().__init__(credmgr, id, appName, enabled, ownerId)
        self.dsn = dsn

    @staticmethod
    @resolveUser()
    def _create(_credmgr, appName=None, dsn=None, owner=None):
        '''Create a new Sentry Token

        **PERMISSIONS: At least Active user is required.**

        Sentry Tokens are used for logging and error reporting in applications

        :param str appName: Name of the Sentry Token (required)
        :param str dsn: DSN of the Sentry Token (required)
        :param Union[User,int,str] owner: Owner of the verification. Requires Admin to create for other users.
        :return: SentryToken
        '''
        data = {'app_name': appName, 'dsn': dsn}
        if owner:
            data['owner_id'] = owner
        return _credmgr.post('/sentry_tokens', data=data)