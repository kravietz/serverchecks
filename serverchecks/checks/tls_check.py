import socket
import ssl
from datetime import datetime, timedelta
from typing import Optional

from serverchecks import Outcome


def _date(d: str) -> Optional[datetime]:
    try:
        # try decoding locale representation first
        return datetime.strptime(d, '%c')
    except ValueError:
        try:
            # try 'Jan 30 23:00:15 2019 GMT' representation
            return datetime.strptime(d, '%b %d %H:%M:%S %Y %Z')
        except ValueError:
            return None


async def check(host: str, port: int = 443, days: int = 3) -> Outcome:
    context: ssl.SSLContext = ssl.create_default_context()
    timeout: float = 3.0

    try:
        with socket.create_connection((host, port), timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssl_sock:
                cert = ssl_sock.getpeercert()
    except ssl.SSLError as e:
        return Outcome(False, f'TLS error for {host}: {e}')
    else:
        not_before: datetime = _date(cert.get('notBefore'))
        not_after: datetime = _date(cert.get('notAfter'))

        now: datetime = datetime.now()

        if not not_before or not not_after:
            return Outcome(False, f'Unable to determine notBefore or notAfter dates in {cert}')

        if now < not_before:
            return Outcome(False, f'TLS certificate for {host} not valid as {now} is before {not_before}')

        target_date: datetime = now + timedelta(days=days)
        if target_date > not_after:
            return Outcome(False, f'TLS certificate for {host} not valid as {target_date} is after {not_after}')

        return Outcome(True, f'Certificate for {host} valid until {not_after}')
