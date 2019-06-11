import asyncio

from serverchecks import Outcome
from serverchecks.checks import AbstractCheck


class TcpCheck(AbstractCheck):
    name = 'TCP'

    def __init__(self, **kwargs) -> None:
        self.host: str = kwargs.get('host')
        self.port: int = kwargs.get('port')
        self.timeout: float = kwargs.get('timeout', 2.0)

        if self.host is None:
            raise ValueError(f'{self.name} required `host` parameter is missing')

    async def _connect(self):
        return await asyncio.open_connection(self.host, self.port)

    async def check(self) -> Outcome:
        try:
            r, w = await asyncio.wait_for(self._connect(), timeout=self.timeout)
        except asyncio.TimeoutError:
            return Outcome(False, f'TCP connection to {self.host}:{self.port} failed: {e}')
        else:
            w.close()
            await w.wait_closed()
            return Outcome(True, f'TCP cnnection to {self.host}:{self.port} successful')

    def __str__(self):
        return f'<{self.name} {self.host}:{self.port}>'


check_class = TcpCheck
