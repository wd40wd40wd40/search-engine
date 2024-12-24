import asyncio
from urllib.parse import urlparse

from crawler.fetcher import Fetcher
from crawler.parser import Parser
from crawler.robots import RobotsHandler

class Crawler:
    """
    Main crawler class that orchestrates fetching, parsing,
    and adhering to robots.txt rules.
    """

    def __init__(self, start_url, max_pages=50, max_depth=3):
        """
        Initializes the crawler with a starting URL and crawling parameters.
        """
        self.start_url = start_url
        self.max_pages = max_pages
        self.max_depth = max_depth

        self.visited = set()  # Set of visited URLs
        self.queue_URLS_to_Visit = [(start_url, 0)]  # Queue for BFS with (url, depth)

        self.fetcher = Fetcher() # handles fetching the HTML page of web pages, including handling timeouts, redirects, and errors
        self.parser = Parser() # extracts the title and hyperlinks from the fetched HTML content and normalizes URLs
        self.robots_handler = RobotsHandler() # parses and enforces rules from the robots.txt file to respect crawling restrictions

        # Cache of domain -> set of disallowed paths
        self.domain_to_disallowed = {}

    " Parses the URL and returns scheme://netloc so we can look up the correct robots.txt entry. "
    #basically gets the main domain of a website
    #used for robots.txt in case we move to new domain and need to redo robots
    def get_mainAddress(self, url):
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    " Starts the crawling process and orchestrates fetching and parsing. "
    async def crawl(self):
        async with self.fetcher.create_session() as session:
            # Main crawling loop
            while self.queue_URLS_to_Visit and (len(self.visited) < self.max_pages):
                url, depth = self.queue_URLS_to_Visit.pop(0)

                # Skip if we already visited url
                if url in self.visited:
                    continue

                domain = self.get_mainAddress(url)

                # Check if we have robots data for this domain
                if domain not in self.domain_to_disallowed:
                    # Fetch and parse the domain's robots.txt once
                    disallowed_paths = await self.robots_handler.get_disallowed_paths(session, domain)
                    self.domain_to_disallowed[domain] = disallowed_paths

                # If this URL is disallowed, skip
                #look at this line again and understand
                #basically if any part of url restricted it evals to true means wrong path
                disallowed = any(url.startswith(path) for path in self.domain_to_disallowed[domain])
                if disallowed:
                    continue

                # Fetch the page
                html = await self.fetcher.fetch(session, url)
                if html:
                    # Parse the page for title and links
                    title, links = self.parser.parse(html, url)
                    #print(f"Visited: {url}, Title: {title}")

                    # Mark visited
                    self.visited.add(url)

                    # Add new links to the queue
                    if depth < self.max_depth:
                        for link in links:
                            if link not in self.visited:
                                self.queue_URLS_to_Visit.append((link, depth + 1))
                else:
                    print("Something went wrong; Hit the else at end of crawler")
