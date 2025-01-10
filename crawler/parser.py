from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Parser:
    """
    Extracts the page title, main text, and outgoing links from HTML.
    Normalizes URLs using urljoin + urlparse.
    """

    def parse(self, html, base_url):
        soup = BeautifulSoup(html, "lxml")

        # Title or fallback
        title = soup.title.get_text(strip=True) if soup.title else "No Title"

        # description
        meta_description = soup.find('meta', attrs={'name': 'description'})

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

        if meta_description and 'content' in meta_description.attrs:
            description = meta_description['content']
        else:
            description = "No Description"


        # Return all 4 so you have the full page text for indexing
        return title, text, links, description
