import asyncio
import time
from urllib.parse import urlparse
import aiohttp
import ssl
import certifi

from crawler.fetcher import Fetcher
from crawler.parser import Parser
from crawler.robots import RobotsHandler
from indexer.indexer import Indexer

class Crawler:
    """
    Main crawler class that orchestrates fetching, parsing,
    indexing, and adhering to robots.txt rules.
    """

    def __init__(self, start_url, max_pages=50, max_depth=3):
        self.start_url = start_url
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())

        self.visited = set()
        self.queue = [(start_url, 0)]

        self.fetcher = Fetcher()  # concurrency, skipping, etc. can be set in Fetcher()
        self.parser = Parser()
        self.robots_handler = RobotsHandler()
        self.robots_domains = {}

        self.indexer = Indexer()

        self.page_count = 0  # We'll increment for each visited page
        self.overall_start = 0  # We'll store the crawl start time here

    async def crawl(self):
        """
        Main BFS-like crawling loop. Only prints:
          - final index finalization time
          - overall crawl time
          - # of pages crawled, # of tokens indexed
        plus it updates us every 50 pages crawled with how long it took so far.
        """
        self.overall_start = time.perf_counter()

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=self.ssl_context)) as session:
            # BFS-like loop with concurrency
            while self.queue and len(self.visited) < self.max_pages:
                # We'll gather a batch of up to 20
                tasks = []
                batch_size = 20
                next_batch = []

                for _ in range(batch_size):
                    if not self.queue:
                        break
                    url, depth = self.queue.pop(0)
                    next_batch.append((url, depth))

                for url, depth in next_batch:
                    if url in self.visited:
                        continue
                    tasks.append(asyncio.create_task(self.process_url(session, url, depth)))

                if tasks:
                    await asyncio.gather(*tasks)

            # Finalize the index
            start_final = time.perf_counter()
            self.indexer.finalize_index()
            final_time = time.perf_counter() - start_final
            print(f"Index finalization complete. TF–IDF took {final_time:.2f}s")

        total_elapsed = time.perf_counter() - self.overall_start
        print(f"\nCrawl finished.")
        print(f"Total runtime = {total_elapsed:.2f}s")
        print(f"Crawled {len(self.visited)} pages. Indexed {len(self.indexer.inverted_index)} unique tokens.\n")

    async def process_url(self, session, url, depth):
        """
        Process a single URL:
          - Possibly fetch robots.txt
          - Fetch the page
          - Parse the page
          - Index the page
          - Add new links if within max_depth
        """
        parsed = urlparse(url)
        domain = f"{parsed.scheme}://{parsed.netloc}"

        # robots.txt check if domain not known
        if domain not in self.robots_domains:
            try:
                disallowed = await self.robots_handler.get_disallowed_paths(session, domain)
                self.robots_domains[domain] = disallowed
            except Exception:
                self.robots_domains[domain] = []

        disallowed_paths = self.robots_domains.get(domain, [])
        if any(url.startswith(domain + path) for path in disallowed_paths):
            return

        # Fetch
        html = await self.fetcher.fetch(session, url)
        if not html:
            return

        # Mark visited
        self.visited.add(url)
        self.page_count += 1

        # Parse
        title, text, links = self.parser.parse(html, url)

        # Index
        combined_text = (title + " " + text).strip()
        self.indexer.add_document(url, combined_text)
        self.indexer.set_document_title(url, title)
        self.indexer.set_document_full_text(url, combined_text)

        # Only print progress every 50 pages
        if self.page_count % 50 == 0:
            elapsed = time.perf_counter() - self.overall_start
            print(f"[Progress] Crawled {self.page_count} pages so far in {elapsed:.2f}s")

        # BFS queue
        if depth < self.max_depth:
            for link in links:
                if link not in self.visited:
                    self.queue.append((link, depth + 1))
