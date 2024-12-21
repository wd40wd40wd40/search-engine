# crawler/robots.py

class RobotsChecker:
    def __init__(self):
        """
        Initialize a cache for robots.txt rules
        """
        pass

    async def is_allowed(self, url):
        """
        Check if a URL is allowed to be crawled:
        - Fetch and parse robots.txt if not cached
        - Check the rules for disallowed paths
        """
        pass
