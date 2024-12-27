import pytest
from unittest.mock import patch, Mock
from crawler.crawler import Crawler
import asyncio

@pytest.fixture
def crawler():
    return Crawler("https://example.com", max_pages=5, max_depth=2)

@pytest.mark.asyncio
async def test_crawler_initialization(crawler):
    assert crawler.start_url == "https://example.com"
    assert crawler.max_pages == 5
    assert crawler.max_depth == 2
    assert len(crawler.visited) == 0
    assert crawler.queue == [("https://example.com", 0)]

@pytest.mark.asyncio
async def test_crawler_page_links(crawler):
    # Mock the fetcher to return HTML with links
    mock_html_a = "<html><body><a href='https://example.com/pageB'>Link to B</a><a href='https://example.com/pageC'>Link to C</a></body></html>"
    mock_html_b = "<html><body><a href='https://example.com/pageD'>Link to D</a><a href='https://example.com/pageE'>Link to E</a></body></html>"
    mock_html_c = "<html><body><a href='https://example.com/pageD'>Link to D</a><a href='https://example.com/pageE'>Link to E</a></body></html>"
    mock_html_d = "<html><body><a href='https://example.com/pageE'>Link to E</a></body></html>"
    mock_html_e = "<html><body><a href='https://example.com/pageA'>Link to A</a></body></html>"

    # Mock the fetcher to return the appropriate HTML based on the URL
    with patch.object(crawler.fetcher, 'fetch', side_effect=lambda session, url: {
        "https://example.com": mock_html_a,
        "https://example.com/pageB": mock_html_b,
        "https://example.com/pageC": mock_html_c,
        "https://example.com/pageD": mock_html_d,
        "https://example.com/pageE": mock_html_e,
    }.get(url, None)):
        
        await crawler.crawl()  # Start the crawling process

        # Check that all pages were visited
        assert "https://example.com" in crawler.visited
        assert "https://example.com/pageB" in crawler.visited
        assert "https://example.com/pageC" in crawler.visited
        assert "https://example.com/pageD" in crawler.visited
        assert "https://example.com/pageE" in crawler.visited

        # Check that the crawler respects the max_pages limit
        assert len(crawler.visited) <= crawler.max_pages

@pytest.mark.asyncio
async def test_crawler_cycle_detection(crawler):
    # Mock the fetcher to create a cycle
    mock_html_a = "<html><body><a href='https://example.com/pageB'>Link to B</a></body></html>"
    mock_html_b = "<html><body><a href='https://example.com/pageA'>Link to A</a></body></html>"

    with patch.object(crawler.fetcher, 'fetch', side_effect=lambda session, url: {
        "https://example.com": mock_html_a,
        "https://example.com/pageB": mock_html_b,
    }.get(url, None)):
        
        await crawler.crawl()  # Start the crawling process

        # Check that the crawler does not get stuck in a cycle
        assert "https://example.com" in crawler.visited
        assert "https://example.com/pageB" in crawler.visited
        assert len(crawler.visited) == 2  # Should only visit each page once

@pytest.mark.asyncio
async def test_crawler_empty_page(crawler):
    # Mock the fetcher to return an empty page
    mock_html_a = "<html><body></body></html>"

    with patch.object(crawler.fetcher, 'fetch', return_value=mock_html_a):
        await crawler.crawl()  # Start the crawling process

        # Check that the crawler only visits the starting page
        assert "https://example.com" in crawler.visited
        assert len(crawler.visited) == 1  # Only the starting page should be visited

@pytest.mark.asyncio
async def test_crawler_no_links(crawler):
    # Mock the fetcher to return a page with no links
    mock_html_a = "<html><body>No links here!</body></html>"

    with patch.object(crawler.fetcher, 'fetch', return_value=mock_html_a):
        await crawler.crawl()  # Start the crawling process

        # Check that the crawler only visits the starting page
        assert "https://example.com" in crawler.visited
        assert len(crawler.visited) == 1  # Only the starting page should be visited

@pytest.mark.asyncio
async def test_crawler_exceed_max_pages(crawler):
    # Set max_pages to 2 for this test
    crawler.max_pages = 2
    mock_html_a = "<html><body><a href='https://example.com/pageB'>Link to B</a></body></html>"
    mock_html_b = "<html><body><a href='https://example.com/pageC'>Link to C</a></body></html>"
    mock_html_c = "<html><body><a href='https://example.com/pageD'>Link to D</a></body></html>"

    with patch.object(crawler.fetcher, 'fetch', side_effect=lambda session, url: {
        "https://example.com": mock_html_a,
        "https://example.com/pageB": mock_html_b,
        "https://example.com/pageC": mock_html_c,
    }.get(url, None)):
        
        await crawler.crawl()  # Start the crawling process

        # Check that the crawler respects the max_pages limit
        assert len(crawler.visited) <= crawler.max_pages
        assert "https://example.com" in crawler.visited
        assert "https://example.com/pageB" in crawler.visited
        assert "https://example.com/pageC" not in crawler.visited  # Should not visit page C

@pytest.mark.asyncio
async def test_crawler_invalid_url(crawler):
    # Mock the fetcher to simulate an invalid URL
    mock_html_a = "<html><body><a href='https://invalid-url'>Invalid Link</a></body></html>"

    with patch.object(crawler.fetcher, 'fetch', side_effect=lambda session, url: {
        "https://example.com": mock_html_a,
        "https://invalid-url": None,  # Simulate a failed fetch
    }.get(url, None)):
        
        await crawler.crawl()  # Start the crawling process

        # Check that the crawler does not visit the invalid URL
        assert "https://example.com" in crawler.visited
        assert "https://invalid-url" not in crawler.visited  # Should not visit invalid URL
@pytest.mark.asyncio
async def test_crawler_handles_redirects(crawler):
    # This test checks how the crawler handles HTTP redirects.
    mock_html_a = "<html><body><a href='https://example.com/pageB'>Link to B</a></body></html>"
    mock_html_b = "<html><body>Redirecting to <a href='https://example.com/pageC'>Page C</a></body></html>"

    mock_html_c = "<html><body>This is page C</body></html>"

    with patch.object(crawler.fetcher, 'fetch', side_effect=lambda session, url: {
        "https://example.com": mock_html_a,
        "https://example.com/pageB": mock_html_b,
        "https://example.com/pageC": mock_html_c,
    }.get(url, None)):
        await crawler.crawl()
        # Now the crawler *can* fetch pageC and add it to visited
        assert "https://example.com/pageC" in crawler.visited

@pytest.mark.asyncio
async def test_crawler_handles_large_number_of_links(crawler):
    # This test checks how the crawler handles a page with a large number of links.
    links = "".join(f"<a href='https://example.com/page{i}'>Link to Page {i}</a>" for i in range(1, 101))
    mock_html_a = f"<html><body>{links}</body></html>"

    with patch.object(crawler.fetcher, 'fetch', return_value=mock_html_a):
        await crawler.crawl()  # Start the crawling process

        # Check that the crawler visits the first page and respects max_pages
        assert "https://example.com" in crawler.visited
        assert len(crawler.visited) <= crawler.max_pages

@pytest.mark.asyncio
async def test_crawler_handles_non_html_content(crawler):
    # This test checks how the crawler handles non-HTML content (e.g., images, PDFs).
    mock_html_a = "<html><body><a href='https://example.com/image.png'>Image Link</a></body></html>"
    mock_image_response = b'\x89PNG\r\n\x1a\n'  # Mock binary data for an image

    with patch.object(crawler.fetcher, 'fetch', side_effect=lambda session, url: {
        "https://example.com": mock_html_a,
        "https://example.com/image.png": None,
    }.get(url, None)):
        
        await crawler.crawl()  # Start the crawling process

        # Check that the crawler does not visit non-HTML content
        assert "https://example.com/image.png" not in crawler.visited

@pytest.mark.asyncio
async def test_crawler_handles_slow_responses(crawler):
    # This test checks how the crawler handles slow responses from the server.
    mock_html_a = "<html><body><a href='https://example.com/pageB'>Link to B</a></body></html>"

    with patch.object(crawler.fetcher, 'fetch', return_value=mock_html_a):
        await asyncio.sleep(2)  # Simulate a slow response
        await crawler.crawl()  # Start the crawling process

        # Check that the crawler still visits the starting page
        assert "https://example.com" in crawler.visited

@pytest.mark.asyncio
async def test_crawler_stops_after_max_depth(crawler):
    # This test checks that the crawler stops following links after reaching max_depth.
    crawler.max_depth = 1  # Set max_depth to 1
    mock_html_a = "<html><body><a href='https://example.com/pageB'>Link to B</a></body></html>"
    mock_html_b = "<html><body><a href='https://example.com/pageC'>Link to C</a></body></html>"

    with patch.object(crawler.fetcher, 'fetch', side_effect=lambda session, url: {
        "https://example.com": mock_html_a,
        "https://example.com/pageB": mock_html_b,
    }.get(url, None)):
        
        await crawler.crawl()  # Start the crawling process

        # Check that the crawler does not visit page C
        assert "https://example.com/pageC" not in crawler.visited
