import httpx, asyncio, random, time

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0")
}

async def fetch(url, retries=3, cooldown=(1, 3)):
    for i in range(retries):
        try:
            async with httpx.AsyncClient(timeout=15, headers=HEADERS) as client:
                r = await client.get(url)
                r.raise_for_status()
                return r.text
        except httpx.HTTPError:
            if i == retries - 1:
                raise
            await asyncio.sleep(random.uniform(*cooldown))

    