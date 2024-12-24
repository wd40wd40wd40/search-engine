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
        return aiohttp.ClientSession()

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                if 'text/html' in response.headers.get('Content-Type', ''):
                    return await response.text()
                else:
                    return None  # Skip non-HTML content
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
