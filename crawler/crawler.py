# crawler/crawler.py

class Crawler:
    def __init__(self, seed_urls, max_concurrent):
        """
        Initialize the crawler with:
        - A queue for URLs
        - A set for visited URLs
        - Fetcher and RobotsChecker instances
        """
        pass

    async def run(self):
        """
        Manage the crawling process:
        - Use async tasks to fetch pages concurrently
        - Check robots.txt before fetching
        - Extract links and add them to the queue
        - Yield (url, content) pairs
        """
        pass
