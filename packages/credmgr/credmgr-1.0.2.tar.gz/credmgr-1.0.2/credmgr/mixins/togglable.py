from credmgr.models.utils import camelToSnake


class ToggableMixin:
    _enabledAttr = 'enabled'

    def toggle(self, enabled):
        payload = [{'op': 'replace', 'path': f'/{camelToSnake(self._enabledAttr)}', 'value': enabled}]
        self.__dict__.update(self._credmgr.patch(f'{self._path}/{self.id}', data=payload).__dict__)