import asyncio

import aiohttp
from returns.future import future_safe

@future_safe
async def load_page(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.text()

async def main():
    result = await load_page("https://pl.pycon.org/2025/agenda/")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())