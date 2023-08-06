from credmgr.mixins import BaseModel, DeletableMixin, OwnerMixin


class RefreshToken(BaseModel, DeletableMixin, OwnerMixin):
    _attrTypes = {
        **BaseModel._attrTypes,
        'reddit_app_id': 'int',
        'redditor': 'str',
        'refresh_token': 'str',
        'owner_id': 'int',
        'scopes': 'str',
        'issued_at': 'datetime',
        'revoked': 'bool',
        'revoked_at': 'datetime'
    }

    _path = '/refresh_tokens'
    _credmgrCallable = 'refreshToken'
    _fetchNameAttr = {'redditor': 'redditor', 'redditAppId': 'reddit_app_id'}
    _getByNamePath = 'by_redditor'
    _canFetchByName = True
    _nameAttr = 'redditor'

    def __init__(self, credmgr, id=None, redditAppId=None, redditor=None, refreshToken=None, ownerId=None, scopes=None, issuedAt=None, revoked=False, revokedAt=None):
        super().__init__(credmgr, id)
        self.redditAppId = redditAppId
        self.redditApp = self._credmgr.redditApp(self.redditAppId)
        self.redditor = redditor
        self.refreshToken = refreshToken
        self.ownerId = ownerId
        self.scopes = scopes
        self.issuedAt = issuedAt
        self.revoked = revoked
        self.revokedAt = revokedAt