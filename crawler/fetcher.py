import aiohttp
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

class Fetcher:
    """
    Concurrent fetcher that:
      - Skips certain file extensions
      - Truncates large HTML at 100 KB
      - Limits concurrency to 10
    """

    def __init__(
        self,
        concurrency: int = 10,
        timeout: int = 10,
        max_content_size: int = 100_000,  # smaller truncation
    ):
        self.semaphore = asyncio.Semaphore(concurrency)
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_content_size = max_content_size
        self.skip_file_extensions = [
            ".pdf", ".png", ".jpg", ".gif", ".jpeg", ".svg", ".zip", ".rar",
            ".doc", ".docx", ".xls", ".xlsx"
        ]

    async def create_session(self):
        return aiohttp.ClientSession(timeout=self.timeout)

    async def fetch(self, session, url: str):
        # Quick check: skip known binary resources
        lower_url = url.lower()
        if any(lower_url.endswith(ext) for ext in self.skip_file_extensions):
            logging.info(f"Skipping URL due to file extension: {url}")
            return None

        async with self.semaphore:
            try:
                async with session.get(url) as response:
                    if (
                        response.status == 200
                        and "text/html" in response.headers.get("Content-Type", "")
                    ):
                        text = await response.text()
                        # Truncate to 100 KB
                        if len(text) > self.max_content_size:
                            text = text[: self.max_content_size]
                        return text
                    else:
                        return None
            except asyncio.TimeoutError:
                logging.error(f"Timeout fetching {url}")
                return None
            except Exception as e:
                logging.error(f"Error fetching {url}: {e}")
                return None
