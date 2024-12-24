import unittest
from unittest.mock import AsyncMock, patch
from crawler.crawler import Crawler

class TestCrawler(unittest.IsolatedAsyncioTestCase):
    async def test_crawl_single_page(self):
        start_url = 'http://example.com'
        crawler = Crawler(start_url, max_pages=1, max_depth=1)

        with patch.object(crawler.fetcher, 'fetch') as mock_fetch, \
             patch.object(crawler.parser, 'parse') as mock_parse, \
             patch.object(crawler.robots_handler, 'get_disallowed_paths') as mock_robots:

            mock_fetch.return_value = '<html><body></body></html>'
            mock_parse.return_value = ('Test Page', set())
            mock_robots.return_value = set()

            await crawler.crawl()

            self.assertIn(start_url, crawler.visited)
            self.assertEqual(len(crawler.visited), 1)

if __name__ == '__main__':
    unittest.main()
