def test_parser_handles_relative_urls(parser):
    html = "<a href='/relative/path'>Link</a>"
    base_url = "https://example.com"
    title, links = parser.parse(html, base_url)
    assert "https://example.com/relative/path" in links

def test_parser_handles_malformed_html(parser):
    html = "<html><body><a href='broken</a></body>"
    title, links = parser.parse(html, "https://example.com")
    assert isinstance(links, list)
