import json

from . import RedditApp
from .utils import resolveModelFromInput, resolveUser
from ..mixins import BaseModel, DeletableMixin, EditableMixin, OwnerMixin


class UserVerification(BaseModel, DeletableMixin, EditableMixin, OwnerMixin):
    _attrTypes = {
        **BaseModel._attrTypes, 'id': 'int', 'user_id': 'str', 'redditor': 'str', 'reddit_app_id': 'int', 'extra_data': 'dict', 'owner_id': 'int'
    }

    _editableAttrs = ['userId', 'redditor', 'redditAppId', 'extraData']
    _path = '/user_verifications'
    _credmgrCallable = 'userVerification'
    _nameAttr = 'userId'
    _canFetchByName = True
    _getByNamePath = 'get_redditor'
    _fetchNameAttr = 'user_id'

    def __init__(self, credmgr, id=None, userId=None, redditor=None, redditAppId=None, extraData=None, ownerId=None):
        super().__init__(credmgr, id)
        self.userId = userId
        self.redditAppId = redditAppId
        self.redditApp = self._credmgr.redditApp(self.redditAppId)
        if redditor:
            self.redditor = redditor
        if extraData:
            self.extraData = extraData
        self.ownerId = ownerId

    @staticmethod
    @resolveUser()
    def _create(_credmgr, userId, redditApp, redditor=None, extraData=None, owner=None):
        '''Create a new User Verification

        **PERMISSIONS: At least Active user is required.**

        User Verifications for verifying a redditor with a User ID

        :param str userId: User ID to associate Redditor with (required)
        :param Union[RedditApp,int,str] redditApp: Reddit app the User Verification is for (required)
        :param str redditor: Redditor the User Verification is for. This is not usually set manually.
        :param dict extraData: Extra JSON data to include with verification
        :param Union[User,int,str] owner: Owner of the verification. Requires Admin to create for other users.
        :return: UserVerification
        '''

        data = {'user_id': userId, 'reddit_app_id': resolveModelFromInput(_credmgr, RedditApp, redditApp)}
        if redditor:
            data['redditor'] = redditor
        if extraData:
            data['extra_data'] = json.dumps(extraData)
        if owner:
            data['owner_id'] = owner
        return _credmgr.post('/user_verifications', data=data)