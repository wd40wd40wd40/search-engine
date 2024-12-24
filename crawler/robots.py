import aiohttp
from urllib.parse import urljoin

class RobotsHandler:
    " Handles parsing and applying rules from robots.txt. "

    async def get_disallowed_paths(self, session, base_url):
        " Fetches and parses robots.txt for disallowed paths. "
        disallowed = set()
        robots_url = urljoin(base_url, "/robots.txt")  # Construct the robots.txt URL
        try:
            async with session.get(robots_url) as response:
                if response.status == 200:
                    for line in (await response.text()).splitlines():
                        line = line.strip()
                        if line.lower().startswith("disallow:"):
                            path = line.split(":", 1)[1].strip()
                            disallowed.add(urljoin(base_url, path))
        except Exception:
            pass  # Robots.txt is optional and failures are non-critical
        return disallowed
