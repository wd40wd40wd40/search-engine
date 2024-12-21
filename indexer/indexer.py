# indexer/indexer.py

class Indexer:
    def __init__(self):
        """
        Initialize a storage system for the reverse index
        """
        pass

    def index_document(self, url, content):
        """
        Tokenize and index a document:
        - Tokenize the content into words
        - Add the tokens to the reverse index
        """
        pass

    def finalize(self):
        """
        Compute TF-IDF scores for all tokens:
        - Calculate IDF for each term
        - Compute the final TF-IDF score for each token-document pair
        """
        pass

    def get_index(self):
        """
        Return the reverse index
        """
        pass
