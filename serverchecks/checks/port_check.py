import socket

from serverchecks import Outcome
from serverchecks.checks import AbstractCheck


class PortCheck(AbstractCheck):
    def __init__(self, **kwargs) -> None:
        self.host: str = kwargs.get('host')
        self.port: int = kwargs.get('port')
        self.timeout: float = kwargs.get('timeout', 2.0)

    async def check(self) -> Outcome:
        try:
            with socket.create_connection((self.host, self.port), self.timeout) as sock:
                return Outcome(True, f'TCP cnnection to {self.host}:{self.port} successful')
        except OSError as e:
            return Outcome(False, f'TCP connection to {self.host}:{self.port} failed: {e}')


check_class = PortCheck
