# search-engine

### Important concepts:
1. Crawler (How it functions)
2. Lemmatization
3. Reverse Indexing
4. Concurrency/Parrallelism
5. Robots.txt
6. TF-IDF
7. Storage
8. Normalizing links (Links don't lead to same location)
9. Stopword elimination

### Future Improvements:
Crawler:
1. Add a database to store previously crawled data with a time of crawl attached. Can then set condition to recrawl
   after set amount of time or manual update. Temporarily, we are storing the crawled data in a JSON file.

### Potential Issues:
Crawler:
1. The way we store crawled links is through the set in an object. This isn't very scalable and we might overflow.
   Not sure where but there will be a limit. Consider switching to some sort of storage system.
2. Not using "title" when returning when parsing in crawler for both parser.py and crawler.py. If we end up not
   using this remove it for performance.

Overall:
1. Cleanup the organization of the project, looks disgusting.

Indexer:
1. Consider using spaCy instead of NLTK for lemmatization


### Current Project Track:
Backend:
1. Build Crawler ✅
   - Test Crawler ✅
3. Add reverse indexing ✅
   - Test reverse indexing ✅
4. Add ranking (TF-IDF) ✅
   - Test Ranking ✅

Frontend:
1. Setup website ✅
2. Setup search and crawling for user input and press ✅
3. Test it ✅
4. Connect it to backend ✅


Design Choices:
1. Break up core logic into 3 main parts: crawling, reverse indexing, and ranking.
2. Dynamic robots.txt domain fetching in case we end off original website
3. Modularity in our code to make choices plug and play for easier/quicker debugging and testing
4. Make reverse indexing after crawling for scalability.
   - Crawling and indexing are different processes making easier to debug
   - Flexibility to not have to recrawl data to reverse index
   - Decoupling the work so it can be worked on by more than one system at a
   time and adequate resources can be provided on a need basis to avoid bottlenecks.
5. Crawler only keeps the urls and not the content for indexer to then go over. Results in fetching 2x for
   everything, but maintains freshness since indexing operates on its own. Also, substantially less storage
   consumption. We're broke students, we can't fund that currently.
