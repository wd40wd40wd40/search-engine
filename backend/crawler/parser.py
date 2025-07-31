from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class Parser:
    """
    Extracts the page title, main text, and outgoing links from HTML.
    Normalizes URLs using urljoin + urlparse.
    """

    def parse(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")

        # Title or fallback
        title = soup.title.get_text(strip=True) if soup.title else "No Title"

        # Remove <script> and <style> tags so they don’t clutter the text
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        # Extract the visible text
        text = soup.get_text(separator=' ', strip=True)

        # Collect and normalize links
        links = set()
        for anchor in soup.find_all('a', href=True):
            link = urljoin(base_url, anchor["href"])
            parsed_url = urlparse(link)

            # We remove trailing slash in path, etc., as a simple normalization
            normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rstrip('/')}"
            links.add(normalized_url)

        # Return all 3 so for full page text for indexing
        return title, text, links
