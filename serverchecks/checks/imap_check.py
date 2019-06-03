import imaplib
from typing import Optional

from serverchecks import Outcome


def _imap_test(imap: imaplib.IMAP4, user: Optional[str] = None, password: Optional[str] = None):
    if not len(imap.capabilities) > 0:
        return Outcome(False, f'IMAP capabilities are empty on {imap.host}:{imap.port}: {imap.capabilities}')

    if not user:
        return Outcome(True, f'IMAP test successful on {imap.host}:{imap.port} (not authenticated)')

    if not imap.login(user, password):
        return Outcome(False, f'IMAP login failed on {imap.host}:{imap.port}')

    imap.select()
    status, messages = imap.search(None, 'ALL')
    if status != 'OK':
        return Outcome(False, f'Cannot search messages on {imap.host}:{imap.port}')

    imap.close()

    return Outcome(True, f'IMAP test successful on {imap.host}:{imap.port} (authenticated)')


async def check(server: str, user: Optional[str] = None, password: Optional[str] = None):
    imap = imaplib.IMAP4_SSL(server)

    return _imap_test(imap, user, password)


async def imap_test(server: str, user: Optional[str] = None, password: Optional[str] = None):
    imap = imaplib.IMAP4(server)

    if not imap.starttls():
        return Outcome(False, f'STARTTLS failed on {imap.host}:{imap.port}')

    return _imap_test(imap, user, password)
