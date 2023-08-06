from . import Bot, DatabaseCredential, RedditApp, RefreshToken, SentryToken, User, UserVerification
from .utils import resolveUser
from ..exceptions import InitializationError
from ..mixins import BaseModel


class Paginator:

    @resolveUser()
    def __init__(self, credmgr, model, batchSize=20, limit=None, itemsOwner=None):
        '''Initialize a ListGenerator instance.

        :param credmgr: An instance of :class:`.CredentialManager`.
        :param model: A CredentialManager model to list.
        :param int batchSize: The number of items to fetch at a time. If ``batchSize`` is None, it will fetch them 100 at a time. (default: 20).
        :param int limit: The maximum number of items to get.
        :param Union[int, User, str] itemsOwner: Owner to filter the items by.
        '''
        self._credmgr = credmgr
        self._model = model(self._credmgr)
        self.batchSize = batchSize
        self.limit = limit
        self.itemsOwner = itemsOwner
        self._itemsReturned = 0
        self._completed = False
        self._offset = 0
        self._currentItemIndex = None
        self._response = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit is not None and self._itemsReturned >= self.limit:
            raise StopIteration() # pragma: no cover

        if self._response is None or self._currentItemIndex >= len(self._response):
            self._next()

        self._currentItemIndex += 1
        self._itemsReturned += 1
        return self._response[self._currentItemIndex - 1]

    def _next(self):
        if self._completed:
            raise StopIteration()
        params = dict(limit=self.batchSize, offset=self._offset)
        if self.itemsOwner:
            params['owner_id'] = self.itemsOwner
        self._response = self._credmgr.get(self._model._path, params=params)
        self._currentItemIndex = 0
        if not self._response:
            raise StopIteration() # pragma: no cover
        if self._response and len(self._response) == self.batchSize:
            self._offset += self.batchSize # pragma: no cover
        else:
            self._completed = True

class BaseHelper(BaseModel):
    _model = None

    def __call__(self, id=None, name=None, batchSize=20, limit=None, owner=None):
        kwargs = {}
        byName = False
        if isinstance(id, str):
            byName = True
            name = id
            id = None
        if id:
            kwargs['id'] = id
        if name:
            if self._model._canFetchByName:
                kwargs[self._model._nameAttr] = name
            else:
                raise InitializationError(f'Cannot get {self._model.__name__!r} by name')
        if not (id or name):
            return self._model(self._credmgr).listItems(batchSize=batchSize, limit=limit, owner=owner)
        item = self._model(self._credmgr, **kwargs)
        item._fetch(byName)
        return item

class UserHelper(BaseHelper):
    _model = User

    def __call__(self, id=None, name=None, batchSize=20, limit=None):
        kwargs = {}
        byName = False
        if isinstance(id, str):
            byName = True
            name = id
            id = None
        if id:
            kwargs['id'] = id
        if name:
            kwargs['username'] = name
        if not (id or name):
            return User(self._credmgr).listItems(batchSize=batchSize, limit=limit)
        item = User(self._credmgr, **kwargs)
        item._fetch(byName)
        return item

    def create(self, username, password, defaultSettings=None, isAdmin=False, isActive=True, isRegularUser=True, isInternal=False, redditUsername=None) -> User:
        '''Create a new user

        **PERMISSIONS: Admin role is required.**

        :param str username: Username for new user (Example: ```spaz```) (required)
        :param str password: Password for new user (Example: ```supersecurepassword```) (required)
        :param dict defaultSettings: Default values to use for new apps (Example: ```{"databaseFlavor": "postgres", "databaseHost": "localhost"}```)
        :param bool isAdmin: Is the user an admin? Allows the user to see all objects and create users (Default: ``False``)
        :param bool isActive: Is the user active? Allows the user to sign in (Default: ``True``)
        :param bool isRegularUser: (Internal use only)
        :param bool isInternal: (Internal use only)
        :param str redditUsername:
        :return: User
        '''

        return self._model._create(self._credmgr, username=username, password=password, defaultSettings=defaultSettings, isAdmin=isAdmin, isActive=isActive, isRegularUser=isRegularUser, isInternal=isInternal, redditUsername=redditUsername)

class BotHelper(BaseHelper):
    _model = Bot

    def create(self, appName, redditApp=None, sentryToken=None, databaseCredential=None, owner=None) -> Bot:
        '''Create a new Bot

        **PERMISSIONS: At least Active user is required.**

        Bots are used for grouping apps into a single request

        :param str appName: Name of the Bot (required)
        :param Union[RedditApp,int] redditApp: Reddit App the bot will use
        :param Union[SentryToken,int] sentryToken: Sentry Token the bot will use
        :param Union[DatabaseCredential,int] databaseCredential: Database Credentials the bot will use
        :param Union[User,int,str] owner: Owner of the bot. Requires Admin to create for other users.
        :return: Bot
        '''

        return self._model._create(self._credmgr, name=appName, redditApp=redditApp, sentryToken=sentryToken, databaseCredential=databaseCredential, owner=owner)

class RedditAppHelper(BaseHelper):
    _model = RedditApp

    def create(self, appName, clientId, userAgent=None, appType='web', redirectUri='https://credmgr.jesassn.org/oauth2/reddit_callback', clientSecret=None, shortName=None,
            appDescription=None, enabled=True, owner=None) -> RedditApp:
        '''Create a new RedditApp

        **PERMISSIONS: At least Active user is required.**

        Reddit Apps are used for interacting with reddit

        :param str appName: (required)
        :param str clientId: Client ID of the Reddit App (required)
        :param str userAgent: User agent used for requests to Reddit's API (required, defaults to user set default, then to 'python:{appName} by /u/{redditUsername}' if currentUser.redditUsername is set or 'python:{appName}' if it is not set)
        :param str appType: Type of the app. One of `web`, `installed`, or `script` (default: 'web')
        :param str redirectUri: Redirect URI for Oauth2 flow. Defaults to user set redirect uri (default: 'https://credmgr.jesassn.org/oauth2/reddit_callback')
        :param str clientSecret: Client secret of the Reddit App
        :param str shortName: Short name of the Reddit App
        :param str appDescription: Description of the Reddit App
        :param bool enabled: Allows the app to be used
        :param Union[User,int,str] owner: Owner of the Reddit App. Requires Admin to create for other users.
        :return: RedditApp
        '''
        if not userAgent:
            redditUsername = self._credmgr.currentUser.redditUsername
            redditUsernameStr = ''
            if redditUsername:
                redditUsernameStr = f' by /u/{redditUsername}'
            userAgent = self._credmgr.getUserDefault('user_agent', f'python:{appName}{redditUsernameStr}')
        return self._model._create(self._credmgr, appName=appName, clientId=clientId, userAgent=userAgent, appType=appType, redirectUri=redirectUri, clientSecret=clientSecret, shortName=shortName, appDescription=appDescription, enabled=enabled, owner=owner)

class UserVerificationHelper(BaseHelper):
    _model = UserVerification

    def create(self, userId, redditApp, redditor=None, extraData=None, owner=None) -> UserVerification:
        '''Create a new User Verification

        **PERMISSIONS: At least Active user is required.**

        User Verifications for verifying a redditor with a User ID

        :param str userId: User ID to associate Redditor with (required)
        :param Union[RedditApp,int,str] redditApp: Reddit app the User Verification is for (required)
        :param str redditor: Redditor the User Verification is for
        :param dict extraData: Extra JSON data to include with verification
        :param int owner: Owner of the verification. Requires Admin to create for other users.
        :return: UserVerification
        '''
        return self._model._create(self._credmgr, userId=userId, redditApp=redditApp, redditor=redditor, extraData=extraData, owner=owner)

    def __call__(self, userId=None, redditAppId=None, batchSize=20, limit=None, owner=None):
        kwargs = {}
        if userId:
            kwargs['userId'] = userId
        if redditAppId:
            kwargs['redditAppId'] = redditAppId
        if not userId:
            return self._model(self._credmgr).listItems(batchSize=batchSize, limit=limit, owner=owner)
        item = self._model(self._credmgr, **kwargs)
        item._fetch(True)
        return item

class SentryTokenHelper(BaseHelper):
    _model = SentryToken

    def create(self, appName, dsn, owner=None) -> SentryToken:
        '''Create a new Sentry Token

        **PERMISSIONS: At least Active user is required.**

        Sentry Tokens are used for logging and error reporting in applications

        :param str appName: Name of the Sentry Token (required)
        :param str dsn: DSN of the Sentry Token (required)
        :param Union[User,int,str] owner: Owner of the verification. Requires Admin to create for other users.
        :return: SentryToken
        '''
        return self._model._create(self._credmgr, appName=appName, dsn=dsn, owner=owner)

class DatabaseCredentialHelper(BaseHelper):
    _model = DatabaseCredential

    def create(self, appName, databaseFlavor='postgres', database='postgres', databaseHost='localhost', databasePort=5432, databaseUsername='postgres', databasePassword=None,
            useSSH=False, sshHost=None, sshPort=None, sshUsername=None, sshPassword=None, useSSHKey=False, privateKey=None, privateKeyPassphrase=None, enabled=True,
            owner=None) -> DatabaseCredential:
        '''Create a new Database Credential

        **PERMISSIONS: At least Active user is required.**

        Database Credentials are used for..ya know..databases

        :param str appName: Name of the Database Credential (required)
        :param str databaseFlavor: Type of database, (default: ``postgres``)
        :param str database: Working database to use, (default: ``postgres``)
        :param str databaseHost: Database server address, (default: ``localhost``)
        :param int databasePort: Port the database server listens on, (default: ``5432``)
        :param str databaseUsername: Username to use to connect to the database
        :param str databasePassword: Password to use to connect to the database
        :param bool useSSH: Determines if the database will be connected to through a tunnel
        :param str sshHost: The address of the server that the SSH tunnel will connect to
        :param str sshPort: The port the SSH tunnel will use
        :param str sshUsername: Username for the SSH tunnel
        :param str sshPassword: Password for the SSH tunnel
        :param bool useSSHKey: Allows the credentials to be used
        :param str privateKey: SSH private key. Note: No validation will be performed.
        :param str privateKeyPassphrase: Passphrase for the SSH key
        :param bool enabled: Allows the credentials to be used
        :param Union[User,int,str] owner: Owner of the app. Requires Admin to create for other users.
        :return: DatabaseCredential
        '''
        return self._model._create(self._credmgr, appName=appName, databaseFlavor=databaseFlavor, database=database, databaseHost=databaseHost, databasePort=databasePort,
            databaseUsername=databaseUsername, databasePassword=databasePassword, useSsh=useSSH, sshHost=sshHost, sshPort=sshPort, sshUsername=sshUsername, sshPassword=sshPassword,
            useSshKey=useSSHKey, privateKey=privateKey, privateKeyPassphrase=privateKeyPassphrase, enabled=enabled, owner=owner)

class RefreshTokenHelper(BaseHelper):
    _model = RefreshToken

    def __call__(self, redditor=None, redditAppId=None, batchSize=20, limit=None, owner=None):
        kwargs = {}
        if redditor:
            kwargs['redditor'] = redditor
        if redditAppId:
            kwargs['redditAppId'] = redditAppId
        if not (redditor and redditAppId):
            return self._model(self._credmgr).listItems(batchSize=batchSize, limit=limit, owner=owner)
        item = self._model(self._credmgr, **kwargs)
        item._fetch(True)
        return item