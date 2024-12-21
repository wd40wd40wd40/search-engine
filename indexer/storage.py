# indexer/storage.py

class Storage:
    def add_document(self, doc_url, tokens):
        """
        Add a document and its tokens to the reverse index
        """
        pass

    def compute_tfidf(self):
        """
        Compute TF-IDF scores for all token-document pairs
        """
        pass

    def get_index(self):
        """
        Return the reverse index with computed scores
        """
        pass
