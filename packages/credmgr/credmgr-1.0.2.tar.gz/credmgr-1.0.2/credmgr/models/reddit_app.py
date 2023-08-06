import base64

import praw

from .utils import resolveModelFromInput, resolveUser
from ..mixins import BaseApp


class RedditApp(BaseApp):
    _attrTypes = {
        **BaseApp._attrTypes,
        'client_id': 'str',
        'client_secret': 'str',
        'short_name': 'str',
        'app_description': 'str',
        'user_agent': 'str',
        'app_type': 'str',
        'redirect_uri': 'str',
        'state': 'str'
        }

    _editableAttrs = BaseApp._editableAttrs + ['clientId', 'clientSecret', 'shortName', 'appDescription', 'userAgent', 'appType', 'redirectUri']
    _path = '/reddit_apps'
    _credmgrCallable = 'redditApp'

    def __init__(self, credmgr, id=None, appName=None, clientId=None, clientSecret=None, shortName=None, appDescription=None, userAgent=None,
                 appType=None, redirectUri=None, state=None, enabled=None, ownerId=None):
        super(RedditApp, self).__init__(credmgr, id, appName, enabled, ownerId)
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.shortName = shortName
        self.appDescription = appDescription
        self.userAgent = userAgent
        self.appType = appType
        self.redirectUri = redirectUri
        self.state = state
        if state:
            self._fetched = True
        self.enabled = enabled
        self.ownerId = ownerId

    @staticmethod
    @resolveUser()
    def _create(_credmgr, appName, clientId, userAgent, appType, redirectUri, clientSecret, shortName, appDescription, enabled, owner=None):
        '''Create a new Reddit App

        **PERMISSIONS: At least Active user is required.**   Reddit Apps are used for interacting with reddit

        :param str appName: (required)
        :param str clientId: Client ID of the Reddit App (required)
        :param str userAgent: User agent used for requests to Reddit's API (required)
        :param str appType: Type of the app. One of `web`, `installed`, or `script` (required)
        :param str redirectUri: Redirect URI for Oauth2 flow. Defaults to user set redirect uri (required)
        :param str clientSecret: Client secret of the Reddit App
        :param str shortName: Short name of the Reddit App
        :param str appDescription: Description of the Reddit App
        :param bool enabled: Allows the app to be used
        :param Union[User,int,str] owner: Owner of the bot. Requires Admin to create for other users.
        :return: RedditApp
        '''
        data = {'app_name': appName, 'client_id': clientId, 'user_agent': userAgent, 'app_type': appType, 'redirect_uri': redirectUri}
        if clientSecret:
            data['client_secret'] = clientSecret
        if shortName:
            data['short_name'] = shortName
        if appDescription:
            data['app_description'] = appDescription
        if enabled:
            data['enabled'] = enabled
        if owner:
            data['owner_id'] = owner
        return _credmgr.post('/reddit_apps', data=data)

    def reddit(self, redditor=None) -> praw.reddit:
        refreshToken = None
        if redditor:
            refreshToken = self._credmgr.refreshToken(redditor, self.id)
            if refreshToken:
                refreshToken = refreshToken.refreshToken
        return praw.Reddit(client_id=self.clientId, client_secret=self.clientSecret, user_agent=self.userAgent, redirect_uri=self.redirectUri, refresh_token=refreshToken)

    def genAuthUrl(self, scopes=None, permanent=False, userVerification=None):
        '''Generates an URL for users to verify or authenciate their Reddit account

        :param Union[list,str] scopes: List of scopes needed. Pass ``'all'`` for all scopes. The ``identity`` scope will always be included. (default: ``['identity']``)
        :param bool permanent: Determines if a refresh token will be provided. (default: ``False``)
        :param Union[UserVerification,int,str] userVerification: Link to a :class:`.UserVerification` object. Accepted values are:

            - An :class:``.UserVerification`` object
            - An :class:``.UserVerification`` id
            - An ``userId`` of a :class:``.UserVerification`` record.
         If a :class:`.UserVerification` record does not exist, one will be created.
        :return str: Auth URL
        '''
        from credmgr.models import UserVerification
        if scopes is None or scopes == 'identity':
            scopes = ['identity']
        elif scopes == 'all':
            scopes = ['*']
        if not 'identity' in scopes and scopes != ['*']:
            scopes = [scopes, 'identity']
        if permanent:
            duration = 'permanent'
        else:
            duration = 'temporary'
        uVerification = resolveModelFromInput(self._credmgr, UserVerification, userVerification, 'userId')
        if not uVerification and userVerification:
            uVerification = self._credmgr.userVerification.create(userVerification, self.id)
        if uVerification:
            state = base64.urlsafe_b64encode(f'{self.state}:{uVerification}'.encode()).decode()
        else:
            state = self.state
        return self.reddit().auth.url(scopes, state, duration)