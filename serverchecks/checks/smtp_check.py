import smtplib
import socket
from email.message import EmailMessage
from typing import Optional

from serverchecks import Outcome


async def check(server: str, user: Optional[str] = None, password: Optional[str] = None, port: int = 25):
    try:
        smtp = smtplib.SMTP(server, timeout=2.0, port=port)
    except socket.timeout as e:
        return Outcome(False, f'SMTP {server}:{port} timed out: {e}')

    # STARTTLS usually requires EHLO
    smtp.ehlo('example.com')

    try:
        smtp.starttls()
    except smtplib.SMTPNotSupportedError as e:
        return Outcome(False, f'SMTP STARTTLS failed on {server}:{port}: {e}')

    auth = 'not authenticated'

    if user:
        msg = EmailMessage()
        msg.set_content('test')
        msg['From'] = user
        msg['To'] = user
        msg['Subject'] = 'test'

        smtp.login(user, password)
        smtp.send_message(msg, user, user)

        auth = 'authenticated'

    smtp.quit()

    return Outcome(True, f'SMTP successful on {server}:{port}: {auth}')
