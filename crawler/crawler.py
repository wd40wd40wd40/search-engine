import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


class Crawler:
   def __init__(self, start_url, max_pages=50):
       self.start_url = start_url
       self.max_pages = max_pages
       self.visited = set()  # To keep track of visited URLs
       self.queue = deque([start_url])  # Queue for BFS traversal


   async def fetch_and_process(self, session, url):
       """Fetch and process a single URL."""
       try:
           async with session.get(url) as response:
               html = await response.text()


               # Parse the page
               soup = BeautifulSoup(html, 'html.parser')


               # Print the current URL and its title
               print(f"Crawling: {url}")
               print(f"Title: {soup.title.string if soup.title else 'No Title'}\n")


               # Add the URL to the visited set
               self.visited.add(url)


               # Find all links on the page
               for link in soup.find_all('a', href=True):
                   full_url = urljoin(url, link['href'])  # Handle relative URLs


                   # Normalize URL to avoid duplicates (remove fragments and query params)
                   parsed_url = urlparse(full_url)
                   normalized_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path


                   # Add the link to the queue if it hasn't been visited yet
                   if normalized_url not in self.visited and parsed_url.netloc:  # Skip empty or external links
                       self.queue.append(normalized_url)


       except Exception as e:
           # Print error message if a request fails
           print(f"Failed to fetch {url}: {e}\n")


   async def crawl(self):
       print(f"Starting crawl at: {self.start_url}\n")


       async with aiohttp.ClientSession() as session:
           while self.queue and len(self.visited) < self.max_pages:
               url = self.queue.popleft()


               if url not in self.visited:
                   await self.fetch_and_process(session, url)


