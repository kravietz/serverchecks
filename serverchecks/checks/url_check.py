import socket
from urllib.error import URLError
from urllib.request import urlopen

from serverchecks import Outcome


async def check(url: str, code: int = 200) -> Outcome:
    timeout: float = 3.0
    try:
        ret = urlopen(url, timeout=timeout)
    except (URLError, socket.timeout) as e:
        return Outcome(False, f'URL {url} failed: {e}')
    else:
        ret_code = ret.getcode()
        if ret_code == code:
            return Outcome(True, f'URL {url} returned code {ret_code}')
        else:
            return Outcome(False, f'URL {url} returned code {ret_code} vs expected {code}')
