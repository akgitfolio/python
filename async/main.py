import asyncio
import aiohttp
import logging
from aiohttp import ClientSession
from typing import List


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def fetch_data(url: str, session: ClientSession, retries: int = 3) -> dict:
    for attempt in range(retries):
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                return await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt + 1 == retries:
                return {"error": str(e)}
        await asyncio.sleep(2**attempt)


async def fetch_all(urls: List[str], concurrency: int = 5) -> List[dict]:
    semaphore = asyncio.Semaphore(concurrency)
    async with ClientSession() as session:
        tasks = [fetch_with_semaphore(url, session, semaphore) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


async def fetch_with_semaphore(
    url: str, session: ClientSession, semaphore: asyncio.Semaphore
) -> dict:
    async with semaphore:
        return await fetch_data(url, session)


async def main():
    urls = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/comments/1",
    ]
    try:
        results = await fetch_all(urls)
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                logging.error(f"Error fetching data from {urls[idx]}: {result}")
            else:
                logging.info(f"Data from {urls[idx]}:")
                logging.info(result)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
