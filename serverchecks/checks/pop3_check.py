import poplib
from typing import Optional, Union

from serverchecks import Outcome
from serverchecks.checks import AbstractCheck


class Pop3Check(AbstractCheck):

    def __init__(self, **kwargs) -> None:
        self.pop3_server: str = kwargs.get('pop3_server')
        self.pop3_mode: int = kwargs.get('pop3_mode')
        if self.pop3_mode not in ('pop3s_ssl', 'pop3_starttls'):
            raise ValueError('pop3_mode must be one of pop3_ssl or pop3_starttls')
        self.username: Optional[str] = kwargs.get('username', None)
        self.password: Optional[str] = kwargs.get('password', None)
        self.pop3: Optional[Union[poplib.POP3_SSL, poplib.POP3]] = None

    async def check(self) -> Outcome:
        if self.pop3_mode == 'pop3s_ssl':
            self.pop3 = poplib.POP3_SSL(self.pop3_server)
        else:
            self.pop3 = poplib.POP3(self.pop3_server)

            try:
                self.pop3.stls()
            except poplib.error_proto as e:
                return Outcome(False, f'STARTTLS failed on {self.pop3.host}:{self.pop3.port}: {e}')

        if not len(self.pop3.capa().items()) > 0:
            return Outcome(False, f'POP3 capabilities empty on {self.pop3.host}:{self.pop3.port}: {self.pop3.capa()}')

        if not self.username:
            self.pop3.close()
            return Outcome(True, f'POP3 test successful on {self.pop3.host}:{self.pop3.port} (not authenticated)')

        try:
            self.pop3.user(self.username)
            self.pop3.pass_(self.password)
        except poplib.error_proto as e:
            return Outcome(False, f'POP3 authentication failed on {self.pop3.host}:{self.pop3.port}: {e}')

        self.pop3.uidl()

        status, messages, num = self.pop3.list()
        if not status.startswith(b'+OK'):
            return Outcome(False, f'POP3 status failed on {self.pop3.host}:{self.pop3.port}: {status}')

        self.pop3.close()


check_class = Pop3Check
