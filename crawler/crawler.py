import asyncio
from urllib.parse import urlparse
from crawler.fetcher import Fetcher
from crawler.parser import Parser
from crawler.robots import RobotsHandler
import aiohttp


" Main crawler class that orchestrates fetching, parsing, and adhering to robots.txt rules. "
class Crawler:
    

    def __init__(self, start_url, max_pages=50, max_depth=3):
        " Initializes the crawler with a starting URL and crawling parameters. "
        self.start_url = start_url
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.visited = set()  # Set of visited URLs
        self.queue = [(start_url, 0)]  # Queue for BFS with (url, depth)

        self.fetcher = Fetcher() # handles fetching HTML content of web pages, including handling timeouts, redirects, and errors
        self.parser = Parser() # extracts the title and hyperlinks from the fetched HTML content and normalizes URLs
        self.robots_handler = RobotsHandler() # parses and enforces rules from the robots.txt file to respect crawling restrictions
        self.robots_domains = {} # Keep the unique domain names in case we move to different site and need to update

    async def crawl(self):
        " Starts the crawling process and orchestrates fetching and parsing. "
        async with aiohttp.ClientSession() as session:
            
            # Main crawling loop
            while self.queue and len(self.visited) < self.max_pages:
                url, depth = self.queue.pop(0)

                # Skip already visited URLs or disallowed paths
                if url in self.visited:
                    continue

                "ROBOTS SETUP"
                # Get domain for robots
                parsedUrl = urlparse(url)
                currDomain = f"{parsedUrl.scheme}://{parsedUrl.netloc}"

                #if new domain encountered then add it to known domains for robots
                if currDomain not in self.robots_domains:
                    try:
                        self.robots_domains[currDomain] = await self.robots_handler.get_disallowed_paths(session, currDomain)
                    except Exception as e:
                        print(f"Error fetching robots.txt for {currDomain}: {e}")
                        disallowedPaths = []  # Default to no disallowed paths if fetch fails
                
                #Get curr robot domain rules
                disallowedPaths = self.robots_domains[currDomain]

                # Skip URLs disallowed by robots.txt
                if any(url.startswith(currDomain + path) for path in disallowedPaths):
                    continue


                # Fetch the HTML content of the page
                html = await self.fetcher.fetch(session, url)
                if html:
                    # Parse the page for title and links
                    title, links = self.parser.parse(html, url)

                    # Mark as visited and add new links to the queue
                    self.visited.add(url)
                    if depth < self.max_depth:
                        for link in links:
                            if link not in self.visited:
                                self.queue.append((link, depth + 1))
