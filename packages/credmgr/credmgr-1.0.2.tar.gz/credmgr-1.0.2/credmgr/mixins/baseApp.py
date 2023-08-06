from ..mixins import BaseModel, DeletableMixin, EditableMixin, OwnerMixin, ToggableMixin


class BaseApp(BaseModel, DeletableMixin, EditableMixin, ToggableMixin, OwnerMixin):
    _attrTypes = {**BaseModel._attrTypes, 'app_name': 'str', 'enabled': 'bool', 'owner_id': 'int'}
    _nameAttr = 'appName'
    _editableAttrs = ['appName', 'enabled']


    def __init__(self, credmgr, id=None, appName=None, enabled=None, ownerId=None):
        super(BaseApp, self).__init__(credmgr, id)
        if appName:
            self.appName = appName
        if enabled is not None:
            self.enabled = enabled
        if ownerId:
            self.ownerId = ownerId