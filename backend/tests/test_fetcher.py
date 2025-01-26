import pytest
import aiohttp
from crawler.fetcher import Fetcher

@pytest.fixture
async def fetcher():
    return Fetcher()

@pytest.mark.asyncio
async def test_fetch_valid_url(fetcher):
    async with aiohttp.ClientSession() as session:
        html = await fetcher.fetch(session, "https://example.com")
        assert html is not None
        assert isinstance(html, str)

@pytest.mark.asyncio
async def test_fetch_invalid_url(fetcher):
    async with aiohttp.ClientSession() as session:
        html = await fetcher.fetch(session, "https://invalid-url-that-does-not-exist.com")
        assert html is None
