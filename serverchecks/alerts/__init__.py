class AbstractAlert:

    async def alert(self, message: str):
        pass

    async def test(self) -> bool:
        pass

    async def close(self) -> None:
        pass
