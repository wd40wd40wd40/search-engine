import math
from collections import defaultdict

from indexer.tokenizer import Tokenizer
from indexer.storage import IndexStorage

class Indexer:
    """
    Maintains a reverse index of term -> {doc_id: term_frequency} in memory,
    computes TF-IDF upon finalization, and stores final scores in IndexStorage.
    """

    def __init__(self):
        self.tokenizer = Tokenizer()       # External library or custom tokenizer
        self.storage = IndexStorage()      # Where we store final TF–IDF and Titles

        # In-memory raw frequency structures:
        self.inverted_index = defaultdict(lambda: defaultdict(int))
        self.doc_lengths = defaultdict(int)
        self.document_count = 0

    def add_document(self, document_id, text):
        """
        Tokenize 'text' and update raw term-frequency counts.
        """
        tokens = self.tokenizer.tokenize(text)
        self.document_count += 1

        freq_map = defaultdict(int)
        for token in tokens:
            freq_map[token] += 1

        for term, count in freq_map.items():
            self.inverted_index[term][document_id] += count

        self.doc_lengths[document_id] = sum(freq_map.values())

    def set_document_title(self, doc_id, title):
        self.storage.set_title(doc_id, title)

    def finalize_index(self):
        """
        Convert raw frequencies into TF–IDF and store them in self.storage.
        """
        N = self.document_count

        for term, doc_map in self.inverted_index.items():
            # doc frequency (# docs containing 'term')
            df = len(doc_map)

            # IDF: log10( N / (df + 1) )  to avoid log of zero
            # or if you prefer exact: log10(N / df) when df>0
            if df > 0:
                idf = math.log10(N / (df + 1))
            else:
                continue

            # Update each doc's frequency -> TF–IDF
            for doc_id, term_freq in doc_map.items():
                tf = term_freq / self.doc_lengths[doc_id]
                tf_idf = tf * idf

                # Store in the final storage
                self.storage.store_value(term, doc_id, tf_idf)

        print("Index finalization complete. TF–IDF scores computed.")

    def save(self, filepath):
        """
        Save the final TF–IDF index to disk (JSON).
        """
        self.storage.save_to_disk(filepath)
