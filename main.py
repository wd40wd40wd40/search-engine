import asyncio
import json
from crawler.crawler import Crawler

async def main():
    # 1) Define your starting URL
    start_url = "https://en.wikipedia.org/wiki/Gokor"

    # 2) Configure how many pages and the depth you want to crawl
    max_pages = 1000
    max_depth = 3

    # 3) Create the crawler instance
    crawler = Crawler(start_url, max_pages, max_depth)

    # 4) Start the crawl (this fetches pages, parses them, and indexes the text)
    await crawler.crawl()

    # 5) After crawling, the index has been finalized. Retrieve it from storage:
    index_data = crawler.indexer.storage.get_index()

    # 6) Print a summary AND save to JSON
    with open("index_data.json", "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False)

    print("Crawl Complete")

    # print(f"\nCrawled {len(crawler.visited)} pages.")
    # print(f"Indexed {len(index_data)} unique tokens.\n")

    # 7) (Optional) Print postings for a sample token
    sample_token = "example"  # or any other word you suspect is in the text
    postings = index_data.get(sample_token, {})
    if postings:
        print(f"Documents containing the token '{sample_token}':")
        for doc_id, tfidf_score in postings.items():
            print(f"  {doc_id} -> TF-IDF: {tfidf_score}")
    else:
        print(f"No documents contain the token '{sample_token}'.")

if __name__ == "__main__":
    asyncio.run(main())
