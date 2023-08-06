from .utils import camelToSnake, resolveUser
from ..mixins import BaseApp


class Bot(BaseApp):
    _attrTypes = {
        **BaseApp._attrTypes, 'reddit_app': 'RedditApp', 'sentry_token': 'SentryToken', 'database_credential': 'DatabaseCredential'
    }
    _editableAttrs = BaseApp._editableAttrs + ['redditAppId', 'sentryTokenId', 'databaseCredentialId']
    _path = '/bots'
    _credmgrCallable = 'bot'
    _canFetchByName = True

    def __init__(self, credmgr, id=None, appName=None, enabled=None, ownerId=None, redditApp=None, sentryToken=None, databaseCredential=None):
        super(Bot, self).__init__(credmgr, id, appName, enabled, ownerId)
        self.redditApp = redditApp
        self.sentryToken = sentryToken
        self.databaseCredential = databaseCredential

    @staticmethod
    @resolveUser()
    def _create(_credmgr, name, redditApp, sentryToken, databaseCredential, owner=None):
        '''Create a new Bot

        **PERMISSIONS: At least Active user is required.**   Bots are used for grouping apps into a single request

        :param str name: Name of the Bot (required)
        :param Union[RedditApp,int] redditApp: Reddit App the bot will use
        :param Union[SentryToken,int] sentryToken: Sentry Token the bot will use
        :param Union[DatabaseCredential,int] databaseCredential: Database Credentials the bot will use
        :param Union[User,int,str] owner: Owner of the bot. Requires Admin to create for other users.
        :return: Bot
        '''

        from . import DatabaseCredential, RedditApp, SentryToken
        additionalParams = {}
        if isinstance(redditApp, RedditApp):
            redditApp = redditApp.id
        if redditApp:
            additionalParams['reddit_app_id'] = redditApp
        if isinstance(sentryToken, SentryToken):
            sentryToken = sentryToken.id
        if sentryToken:
            additionalParams['sentry_token_id'] = sentryToken
        if isinstance(databaseCredential, DatabaseCredential):
            databaseCredential = databaseCredential.id
        if databaseCredential:
            additionalParams['database_credential_id'] = databaseCredential
        if owner:
            additionalParams['owner_id'] = owner
        return _credmgr.post('/bots', data={'app_name': name, **additionalParams})

    def edit(self, **kwargs):
        for key, value in kwargs.items():
            snakeKey = camelToSnake(key)
            if snakeKey in ['reddit_app', 'sentry_token', 'database_credential']:
                newKey = f'{snakeKey}_id'
                kwargs[newKey] = kwargs.pop(key)
        super(Bot, self).edit(**kwargs)