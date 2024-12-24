from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Parser extracts information from the HTML doc 
class Parser:
    # Parse html content and parse all urls
    def parse(self, html, base_url):
        soup = BeautifulSoup(html, "lxml") #object and type of parser we'll use
        title = soup.title.string if soup.title else "No Title" #grab the title
        links = set()

        #extra links and normalize them
        for anchor in soup.find_all('a', href = True):
            link = urljoin(base_url, anchor["href"])  # Combine base with relative url
            parsed_url = urlparse(link)
            normalized_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path.rstrip('/')}"
            links.add(normalized_url)

        return title, links


