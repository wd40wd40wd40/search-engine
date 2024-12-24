import aiohttp
import logging

logging.basicConfig(level=logging.INFO)

class Fetcher:
    """
    Handles HTTP requests and manages connections using aiohttp.
    """

    def __init__(self, timeout=10):
        """
        Initializes the fetcher with a default timeout.
        
        Args:
            timeout (int): Timeout in seconds for HTTP requests.
        """
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def create_session(self):
        """
        Creates an aiohttp session with custom configurations.
        
        Returns:
            aiohttp.ClientSession: An aiohttp session object.
        """
        return aiohttp.ClientSession(timeout=self.timeout)

    async def fetch(self, session, url):
        """
        Fetches the content of a URL.
        
        Args:
            session (aiohttp.ClientSession): The session object for making requests.
            url (str): The URL to fetch.
        
        Returns:
            str: The HTML content of the page or None if an error occurred.
        """
        try:
            async with session.get(url, allow_redirects=True) as response:
                if response.status == 200 and "text/html" in response.headers.get("Content-Type", ""):
                    return await response.text()
                logging.warning(f"Skipping non-HTML or failed URL: {url}")
        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
        return None
