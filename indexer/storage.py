import json
from collections import defaultdict

class IndexStorage:
    """
    Stores the final (token -> {doc_id -> tf_idf}) mapping.
    For large-scale usage, adapt to partial merges on disk or a real DB.
    """

    def __init__(self):
        # token -> { doc_id -> tf_idf }
        self.index_data = defaultdict(dict)

        # title
        self.doc_titles = {}

    def store_value(self, token, doc_id, tf_idf):
        """
        Store the final TF–IDF weight for a (token, doc_id) pair.
        """
        self.index_data[token][doc_id] = tf_idf
    
    def set_title(self, doc_id, title):
        """
        Store the title of the document.
        """
        self.doc_titles[doc_id] = title

    def get_index(self):
        """
        Return the entire index data structure.
        Example:
        {
          "token": {
             "doc_id": 0.123,  # TF–IDF
             ...
          },
          ...
        }
        """
        return {
            "tokens": self.index_data,
            "titles": self.doc_titles
        }
    def save_to_disk(self, filepath):
        """
        Save the index to a JSON file.
        """
        data_to_save = {
            "tokens": {},
            "titles": {}
        }
        for token, docs in self.index_data.items():
            data_to_save[token] = {doc_id: tfidf for doc_id, tfidf in docs.items()}

        data_to_save["titles"] = self.doc_titles

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)

    def load_from_disk(self, filepath):
        """
        Load the index from a JSON file.
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        self.index_data.clear()
        self.doc_titles.clear()
        tokens = loaded.get("tokens", {})
        for token, docs in tokens.items():
            self.index_data[token] = docs
        self.doc_titles = loaded.get("titles", {})

