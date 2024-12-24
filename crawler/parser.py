from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Parser:
    " Extracts links, titles, and other data from HTML content. "

    def parse(self, html, base_url):
        " Parses HTML content and extracts the title and all hyperlinks. "
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else "No Title"
        links = set()

        # Extract and normalize links
        for a_tag in soup.find_all("a", href=True):
            link = urljoin(base_url, a_tag["href"])  # Resolve relative URLs
            parsed_url = urlparse(link)
            normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rstrip('/')}"
            links.add(normalized_url)

        return title, links
