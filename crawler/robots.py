import aiohttp
from urllib.parse import urljoin, urlparse

class RobotsHandler:
    "Handles parsing and applying rules from robots.txt."

    async def get_disallowed_paths(self, session, domain):
        " Fetches and parses robots.txt for a given domain and returns a set of disallowed URLs. "
        disallowed = set()
        robots_url = urljoin(domain, "/robots.txt") # Construct the robots.txt URL

        try:
            async with session.get(robots_url) as response:
                if response.status == 200:
                    text = await response.text()
                    for line in text.splitlines():
                        line = line.strip()
                        if line.lower().startswith("disallow:"):
                            path = line.split(":", 1)[1].strip()
                            # Construct the absolute disallowed URL from domain+path
                            disallowed.add(urljoin(domain, path))
        except Exception:
            pass  # robots.txt is optional, so we silently ignore failures

        return disallowed
