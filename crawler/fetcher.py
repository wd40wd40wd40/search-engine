# crawler/fetcher.py

class Fetcher:
    async def fetch(self, url):
        """
        Fetch a page:
        - Make an HTTP request to the URL
        - Extract links from the response content
        - Return (content, links)
        """
        pass

    def extract_links(self, base_url, html):
        """
        Extract all links from the given HTML:
        - Parse HTML with a library like BeautifulSoup
        - Resolve relative URLs to absolute URLs
        """
        pass
