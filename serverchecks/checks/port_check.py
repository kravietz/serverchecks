import socket

from serverchecks import Outcome


async def port_test(host: str, port: int) -> Outcome:
    timeout: float = 3.0
    try:
        with socket.create_connection((host, port), timeout) as sock:
            return Outcome(True, f'Connection to {host}:{port} successful')
    except OSError as e:
        return Outcome(False, f'Connection to {host}:{port} failed: {e}')
