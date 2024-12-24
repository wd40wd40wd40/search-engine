import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


class Crawler:
    def __init__(self, start_url, max_pages=50):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited = set()
        self.queue = deque([start_url])

    async def fetch_and_process(self, session, url):
        """Fetch and process a single URL."""
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status != 200:
                    print(f"Failed to fetch {url}: HTTP {response.status}")
                    return

                html = await response.text()

                # Parse the page
                soup = BeautifulSoup(html, 'html.parser')

                # Print the current URL and its title
                print(f"Crawling: {url}")
                print(f"Title: {soup.title.string if soup.title else 'No Title'}\n")

                # Add the URL to the visited set
                self.visited.add(url)

                # Find and normalize all links
                for link in soup.find_all('a', href=True):
                    full_url = urljoin(url, link['href'])
                    parsed_url = urlparse(full_url)
                    normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

                    # Add only unvisited and unique URLs to the queue
                    if (
                        normalized_url not in self.visited and
                        normalized_url not in self.queue and
                        parsed_url.netloc
                    ):
                        self.queue.append(normalized_url)

        except aiohttp.ClientConnectorError as e:
            print(f"Network error while fetching {url}: {e}")
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error for {url}: {e.status} {e.message}")
        except asyncio.TimeoutError:
            print(f"Timeout while fetching {url}")
        except Exception as e:
            print(f"Unexpected error for {url}: {e}")

    async def crawl(self):
        print(f"Starting crawl at: {self.start_url}\n")

        async with aiohttp.ClientSession() as session:
            while self.queue and len(self.visited) < self.max_pages:
                url = self.queue.popleft()

                if url not in self.visited:
                    await self.fetch_and_process(session, url)


if __name__ == "__main__":
    start_url = "https://example.com"  # Replace with the starting URL
    max_pages = 50

    crawler = Crawler(start_url, max_pages)
    asyncio.run(crawler.crawl())
