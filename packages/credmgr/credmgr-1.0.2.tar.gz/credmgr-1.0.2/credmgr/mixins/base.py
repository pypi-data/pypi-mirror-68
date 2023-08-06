from datetime import datetime
from credmgr.models.utils import resolveUser


class BaseModel(object):
    _attrTypes = {'id': 'int'}
    _path = None
    _nameAttr = None
    _canFetchByName = False
    _credmgrCallable = None
    _getByNamePath = 'by_name'
    _fetchNameAttr = 'app_name'

    def __init__(self, credmgr, id=None, name=None):
        self._credmgr = credmgr
        self.id = id
        self._fetched = False
        if self._nameAttr and self._canFetchByName:
            setattr(self, self._nameAttr, name)

    def __getattr__(self, attribute): # pragma: no cover
        '''Return the value of `attribute`.'''
        if not attribute.startswith('_') and not self._fetched:
            self._fetch()
            return getattr(self, attribute)
        raise AttributeError(f'{self.__class__.__name__!r} object has no attribute {attribute!r}')

    def get(self, id):
        self.__dict__ = self._credmgr.get(f'{self._path}/{id}').__dict__

    def getByName(self, name):
        data = {}
        if isinstance(self._fetchNameAttr, dict):
            for modelAttr, dataAttr in self._fetchNameAttr.items():
                data[dataAttr] = getattr(self, modelAttr)
        else:
            data[self._fetchNameAttr] = name
        self.__dict__ = self._credmgr.post(f'{self._path}/{self._getByNamePath}', data=data).__dict__

    def _fetch(self, byName=False):
        if byName and self._canFetchByName:
            self.getByName(getattr(self, self._nameAttr))
        else:
            self.get(self.id)
        self._fetched = True

    @resolveUser()
    def listItems(self, batchSize=20, limit=None, owner=None):
        from credmgr.models.helpers import Paginator
        return Paginator(self._credmgr, self.__class__, batchSize=batchSize, limit=limit, itemsOwner=owner)

    def toDict(self):
        result = {}

        for exportAttr, _ in self._attrTypes.items():
            attr = ''.join(exportAttr.split('_')[:1] + [i.capitalize() for i in exportAttr.split('_')[1:]])
            value = getattr(self, attr, None)
            if value:
                if isinstance(value, list):
                    result[exportAttr] = list(map(lambda x: x.toDict() if hasattr(x, 'toDict') else x, value))
                elif hasattr(value, 'toDict'):
                    result[exportAttr] = value.toDict()
                elif isinstance(value, dict):
                    result[exportAttr] = dict(map(lambda item: (item[0], item[1].toDict()) if hasattr(item[1], 'toDict') else item, value.items()))
                elif isinstance(value, datetime):
                    result[exportAttr] = value.astimezone().strftime(self._credmgr.config.dateFormat)
                else:
                    result[exportAttr] = value
        if issubclass(type(self), dict): # pragma: no cover
            for key, value in self.items():
                result[key] = value
        return result

    def __repr__(self): # pragma: no cover
        return f'<{self.__class__.__name__} id={self.id}, {self._nameAttr}={getattr(self, self._nameAttr)!r}>'

    def __eq__(self, other):
        '''Returns true if both objects are equal'''
        if not isinstance(other, type(self)):
            return False

        return self.__dict__ == other.__dict__