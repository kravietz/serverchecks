import asyncio
from concurrent.futures import TimeoutError
from urllib.error import URLError
from urllib.parse import urlparse, ParseResult

import aiohttp

from serverchecks import Outcome
from serverchecks.checks import AbstractCheck


class UrlCheck(AbstractCheck):
    name = 'URL'

    def __init__(self, **kwargs) -> None:
        self.url: str = kwargs.get('url')
        self.url_parsed: ParseResult = urlparse(self.url)
        self.expect_code: int = kwargs.get('expect_code', 200)
        self.timeout: float = kwargs.get('timeout', 30.0)

        allowed = ('http', 'https')
        if self.url_parsed.scheme not in allowed:
            raise ValueError(f'{self.name} only {allowed} schemes are supported: {self.url_parsed.scheme}')

        self.session = aiohttp.ClientSession()

    async def _connect(self):
        async with self.session.get(self.url) as response:
            return response

    async def check(self) -> Outcome:
        try:
            ret = await asyncio.wait_for(self._connect(), timeout=self.timeout)
        except (URLError, TimeoutError) as e:
            return Outcome(False, f'URL {self.url} failed: {e}')
        else:
            ret_code: int = ret.status
            if ret_code == self.expect_code:
                return Outcome(True, f'URL {self.url} returned code {ret_code}')
            else:
                return Outcome(False, f'URL {self.url} returned code {ret_code} vs expected {self.expect_code}')

    def __str__(self):
        return f'<{self.name} {self.url:.20}>'


check_class = UrlCheck
