import aiohttp
import logging

logging.basicConfig(level=logging.INFO)

" Handles HTTP requests and manages connections using aiohttp. "
class Fetcher:  

    def __init__(self, timeout=10):
        "Initializes the fetcher with a default timeout."
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def create_session(self):
        " Creates an aiohttp session with custom configurations. "
        return aiohttp.ClientSession(timeout=self.timeout)

    async def fetch(self, session, url):
        " Fetches the content of a URL. "
        try:
            async with session.get(url, allow_redirects=True) as response:
                if response.status == 200 and "text/html" in response.headers.get("Content-Type", ""):
                    return await response.text()
                logging.warning(f"Skipping non-HTML or failed URL: {url}")
        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
        return None
