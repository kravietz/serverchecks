from telethon import TelegramClient
from telethon.tl.types import User

from serverchecks.alerts import AbstractAlert


class TelegramAlert(AbstractAlert):
    """
    Telegram alert class using Telethon pure-Python MTProto client library

    https://docs.telethon.dev/en/latest/index.html

    The application uses credentials that are obtained from https://my.telegram.org/apps and must be registered
    as a bot with https://t.me/botfather (`bot_token`)
    """
    name = 'Telegram'

    def __init__(self, **kwargs) -> None:
        self.bot_token: str = kwargs.get('bot_token')
        self.api_id: int = int(kwargs.get('api_id'))
        self.api_hash: str = kwargs.get('api_hash')
        self.app_name: str = kwargs.get('app_name')
        self.recipient: str = kwargs.get('recipient')
        self.client = None

    async def _init(self):
        if self.client is None:
            self.client = await TelegramClient(self.app_name, self.api_id, self.api_hash).start(
                bot_token=self.bot_token)

    async def test(self) -> bool:
        await self._init()
        return type(await self.client.get_entity('me')) is User

    async def alert(self, message: str) -> None:
        await self._init()
        await self.client.send_message(self.recipient, message)

    async def close(self) -> None:
        await self.client.disconnect()


alert_class = TelegramAlert
