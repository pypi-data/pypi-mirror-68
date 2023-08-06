from .utils import resolveUser
from ..mixins import BaseApp


class DatabaseCredential(BaseApp):
    _attrTypes = {
        **BaseApp._attrTypes,
        'database_username': 'str',
        'database_host': 'str',
        'database': 'str',
        'database_flavor': 'str',
        'database_port': 'int',
        'database_password': 'str',
        'use_ssh': 'bool',
        'ssh_host': 'str',
        'ssh_port': 'int',
        'ssh_username': 'str',
        'ssh_password': 'str',
        'use_ssh_key': 'bool',
        'private_key': 'str',
        'private_key_passphrase': 'str'
    }

    _editableAttrs = BaseApp._editableAttrs + ['databaseUsername', 'databaseHost', 'database', 'databaseFlavor', 'databasePort', 'databasePassword', 'useSsh', 'sshHost', 'sshPort',
                                               'sshUsername', 'sshPassword', 'useSshKey', 'privateKey', 'privateKeyPassphrase']
    _path = '/database_credentials'
    _credmgrCallable = 'databaseCredential'

    def __init__(self, credmgr, id=None, appName=None, databaseUsername=None, databaseHost=None, database=None, databaseFlavor=None, databasePort=None, databasePassword=None,
            useSsh=None, sshHost=None, sshPort=None, sshUsername=None, sshPassword=None, useSshKey=None, privateKey=None, privateKeyPassphrase=None, enabled=None, ownerId=None):
        super().__init__(credmgr, id, appName, enabled, ownerId)
        self.databaseUsername = databaseUsername
        self.databaseHost = databaseHost
        self.database = database
        self.databasePort = databasePort
        self.enabled = enabled
        self.ownerId = ownerId
        if databaseFlavor:
            self.databaseFlavor = databaseFlavor
        if databasePassword:
            self.databasePassword = databasePassword
        if useSsh:
            self.useSsh = useSsh
        if sshHost:
            self.sshHost = sshHost
        if sshPort:
            self.sshPort = sshPort
        if sshUsername:
            self.sshUsername = sshUsername
        if sshPassword:
            self.sshPassword = sshPassword
        if useSshKey:
            self.useSshKey = useSshKey
        if privateKey:
            self.privateKey = privateKey
        if privateKeyPassphrase:
            self.privateKeyPassphrase = privateKeyPassphrase

    @staticmethod
    @resolveUser()
    def _create(_credmgr, appName, databaseFlavor='postgres', database='postgres', databaseHost='localhost', databasePort=5432, databaseUsername='postgres', databasePassword=None,
            useSsh=False, sshHost=None, sshPort=None, sshUsername=None, sshPassword=None, useSshKey=False, privateKey=None, privateKeyPassphrase=None, enabled=True, owner=None):
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
        :param bool useSsh: Determines if the database will be connected to through a tunnel
        :param str sshHost: The address of the server that the SSH tunnel will connect to
        :param str sshPort: The port the SSH tunnel will use
        :param str sshUsername: Username for the SSH tunnel
        :param str sshPassword: Password for the SSH tunnel
        :param bool useSshKey: Allows the credentials to be used
        :param str privateKey: SSH private key. Note: No validation will be performed.
        :param str privateKeyPassphrase: Passphrase for the SSH key
        :param bool enabled: Allows the credentials to be used
        :param Union[User,int,str] owner: Owner of the app. Requires Admin to create for other users.
        :return: DatabaseCredential
        '''

        data = {}
        if databaseFlavor:
            data['database_flavor'] = databaseFlavor
        if database:
            data['database'] = database
        if databaseHost:
            data['database_host'] = databaseHost
        if databasePort:
            data['database_port'] = databasePort
        if databaseUsername:
            data['database_username'] = databaseUsername
        if databasePassword:
            data['database_password'] = databasePassword
        if useSsh:
            data['use_ssh'] = useSsh
        if sshHost:
            data['ssh_host'] = sshHost
        if sshPort:
            data['ssh_port'] = sshPort
        if sshUsername:
            data['ssh_username'] = sshUsername
        if sshPassword:
            data['ssh_password'] = sshPassword
        if useSshKey:
            data['use_ssh_key'] = useSshKey
        if privateKey:
            data['private_key'] = privateKey
        if privateKeyPassphrase:
            data['private_key_passphrase'] = privateKeyPassphrase
        if enabled:
            data['enabled'] = enabled
        if owner:
            data['owner_id'] = owner
        return _credmgr.post('/database_credentials', data={'app_name': appName, **data})