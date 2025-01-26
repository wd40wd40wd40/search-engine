# ranker/ranker.py

class Ranker:
    def rank(self, query, index):
        """
        Rank documents for a query:
        - Tokenize and lemmatize the query
        - Retrieve documents from the reverse index
        - Compute scores using TF-IDF
        - Return a sorted list of results
        """
        pass
