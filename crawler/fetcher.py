import aiohttp
import logging


#Connect to HTML and manage https connections using aiohttp
class Fetcher:
    # instantiate
    def __init__(self, timeout = 10):
        self.timeout = aiohttp.ClientTimeout(total=timeout) # using a format aiohttp is expecting

    # create the manager to handle connection pooling
    async def create_session(self):
        return aiohttp.ClientSession(timeout = self.timeout)
    
    # Get the content of the url 
    async def fetch(self, session, url): # reuse the session manager to save on efficiency with 'session' as parameter (not opening and closing inside fetch)
        try:
            async with session.get(url, allow_redirects = True) as response: #gives instance of session
                #if succesful connection and is website 
                if response.status == 200 and ("text/html" in response.headers.get("Content-Type", "")):
                    return await response.text()
                logging.warning(f"Skipping non-html or failed URL: {url}")

        except Exception as e:
            logging.error(f"Error fetching {url}: {e}")
        return None
    