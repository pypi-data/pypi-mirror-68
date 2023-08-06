import logging
from typing import List
import json
from email.utils import parseaddr

from cryptography.fernet import Fernet


class Config(object):
    CONFIG_PATH: str = 'config.json'
    DEFAULT_HOSTNAME: str = 'smtp.yandex.ru'
    DEFAULT_PORT: int = 587

    log = logging.getLogger(__name__)

    def __init__(self, filename: str = None):
        self._filename: str = filename or self.CONFIG_PATH
        self.recipients: List[str] = []
        self.hostname: str = self.DEFAULT_HOSTNAME
        self.admin_email: str = ''
        self.server_mail: str = ''
        self.delay: int = 60
        self.port: int = self.DEFAULT_PORT
        self._password: str = ''
        self._enc_key: str = ''
        self._load_from_file()

    @property
    def filename(self):
        return self._filename

    def set_filename(self, filename: str):
        self._filename = filename
        self._load_from_file()

    def asdict(self) -> dict:
        return dict(recipients=self.recipients,
                    hostname=self.hostname,
                    port=self.port,
                    admin_email=self.admin_email,
                    server_mail=self.server_mail,
                    password=self._password,
                    enc_key=self._enc_key
                    )

    def save(self):
        kwargs = self.asdict()
        if all(kwargs.values()):
            with open(self._filename, 'w') as f:
                json.dump(kwargs, f)
        else:
            self.log.error(f'Config is not complete: \n{self}')

    def set_password(self, password: str):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        password = fernet.encrypt(password.encode())
        self._enc_key = key.decode()
        self._password = password.decode()
        self.log.info('Encrypted password is set')

    @property
    def password(self) -> str:
        if not self._password:
            return ''
        return Fernet(self._enc_key.encode()).decrypt(self._password.encode()).decode()

    def set_port(self, port: int):
        if not isinstance(port, int):
            self.log.error(f'Port should be an integer.')
            return
        self.port = port
        self.log.info(f'Port is set: {self.port}.')

    def set_server_mail(self, email: str):
        email = parseaddr(email)[-1]
        if '@' not in email:
            self.log.error(f'Incorrect email: {email}.')
        else:
            self.server_mail = email

    def set_hostname(self, hostname: str):
        self.hostname = hostname
        self.log.info(f'Hostname is set: {self.hostname}')

    def set_admin_email(self, email: str):
        email = parseaddr(email)[-1]
        if '@' not in email:
            self.log.error(f'Incorrect email: {email}.')
        else:
            self.admin_email = email
            self.log.info(f'Admin email is set: {self.admin_email}.')

    def add_recipients(self, emails: List[str]):
        emails_to_add: List[str] = []
        for email in emails:
            email = parseaddr(email)[-1]
            if '@' not in email:
                self.log.error(f'Incorrect email: {email}.')
            else:
                emails_to_add.append(email)
        if emails_to_add:
            self.recipients.extend(emails_to_add)
            self.log.info(f'Successfully added recipients emails: \n{", ".join(emails_to_add)}')

    def remove_recipients(self, emails: List[str]):
        for email in emails:
            if email in self.recipients:
                self.recipients.remove(email)
                self.log.info(f'Recipient email {email} is removed from the list.')
            else:
                self.log.warning(f'Recipient {email} is not in the list.')

    def clear_recipients(self):
        self.recipients = []
        self.log.info(f'Recipient list is cleared.')

    def __repr__(self):
        d = self.asdict()
        args = ['='.join([k, str(v) if not isinstance(v, bytes) else v.decode()])
                for k, v in d.items() if v]
        non_args = ', '.join([k for k, v in d.items() if not v])
        return f'Config({", ".join(args)}); empty parameters: {non_args}'

    def _load_from_file(self):
        try:
            with open(self._filename, 'r') as f:
                config = json.load(f)
                self.recipients = config.get('recipients', self.recipients)
                self.hostname = config.get('hostname', self.hostname)
                self.admin_email = config.get('admin_email', self.admin_email)
                self.server_mail = config.get('server_mail', self.server_mail)
                self._password = config.get('password', self._password)
                self._enc_key = config.get('enc_key', self._enc_key)
                try:
                    self.port = int(config.get('port', self.port))
                except TypeError:
                    self.log.warning(f'Incorrect port: {config.get("port")}. Set to default value')
                    self.port = self.DEFAULT_PORT

        except FileNotFoundError:
            self.log.warning(f'Config file {self._filename} does not exist.')
        except Exception as err:
            self.log.error(f'Unexpected exception occurred while reading config file: {err}.')
