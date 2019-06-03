import imaplib
from typing import Union

from serverchecks import Outcome
from serverchecks.checks import AbstractCheck


class ImapCheck(AbstractCheck):

    def __init__(self, **kwargs) -> None:
        self.imap_server: str = kwargs.get('imap_server')
        self.imap_mode: int = kwargs.get('imap_mode')
        self.username: str = kwargs.get('username', None)
        self.password: str = kwargs.get('password', None)

    async def check(self) -> Outcome:
        self.imap: Union[imaplib.IMAP4_SSL, imaplib.IMAP4] = imaplib.IMAP4_SSL(
            self.imap_server) if self.imap_mode == 'imaps' else imaplib.IMAP4(self.imap_server)

        if not len(self.imap.capabilities) > 0:
            return Outcome(False,
                           f'IMAP capabilities are empty on {self.imap.host}:{self.imap.port}: {self.imap.capabilities}')

        # skip any further tests in non-authenticated mode
        if not self.username:
            return Outcome(True, f'IMAP test successful on {self.imap.host}:{self.imap.port} (not authenticated)')

        if not self.imap.login(self.username, self.password):
            return Outcome(False, f'IMAP login failed on {self.imap.host}:{self.imap.port}')

        self.imap.select()

        status, messages = self.imap.search(None, 'ALL')
        if status != 'OK':
            return Outcome(False, f'Cannot search messages on {self.imap.host}:{self.imap.port}')

        self.imap.close()

        return Outcome(True, f'IMAP test successful on {self.imap.host}:{self.imap.port} (authenticated)')


check_class = ImapCheck
