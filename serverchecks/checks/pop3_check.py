import poplib
from typing import Optional, Union

from serverchecks import Outcome


async def check(server: str, user: Optional[str] = None, password: Optional[str] = None):
    pop3 = poplib.POP3_SSL(server)
    return _pop3_test(pop3, user, password)


async def pop3_test(server: str, user: Optional[str] = None, password: Optional[str] = None):
    pop3 = poplib.POP3(server)

    if not pop3.stls():
        return Outcome(False, f'STARTTLS failed on {pop3.host}:{pop3.port}')

    return _pop3_test(pop3, user, password)


def _pop3_test(pop3: Union[poplib.POP3, poplib.POP3_SSL], user: Optional[str] = None, password: Optional[str] = None):
    if not len(pop3.capa().items()) > 0:
        return Outcome(False, f'POP3 capabilities empty on {pop3.host}:{pop3.port}: {pop3.capa()}')

    if not user:
        pop3.close()
        return Outcome(True, f'POP3 test successful on {pop3.host}:{pop3.port} (not authenticated)')

    try:
        pop3.user(user)
        pop3.pass_(password)
    except poplib.error_proto as e:
        return Outcome(False, f'POP3 authentication failed on {pop3.host}:{pop3.port}: {e}')

    pop3.uidl()
    status, messages, num = pop3.list()
    if not status.startswith(b'+OK'):
        return Outcome(False, f'POP3 status failed on {pop3.host}:{pop3.port}: {status}')

    pop3.close()
