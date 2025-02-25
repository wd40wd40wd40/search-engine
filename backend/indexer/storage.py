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

        # description
        self.doc_fulltext = {}

    def store_value(self, token, doc_id, tf_idf):
        """
        Store the final TF-IDF weight for a (token, doc_id) pair.
        """
        self.index_data[token][doc_id] = tf_idf
    
    def set_title(self, doc_id, title):
        """
        Store the title of the document.
        """
        self.doc_titles[doc_id] = title

    def set_full_text(self, doc_id, full_text):
        """
        Store the description of the document.
        """
        self.doc_fulltext[doc_id] = full_text

    def get_index(self):
        return {
            "tokens": self.index_data,
            "titles": self.doc_titles,
            "full_texts": self.doc_fulltext
        }
    def save_to_disk(self, filepath):
        """
        Save the index to a JSON file.
        """
        data_to_save = {
            "tokens": {},
            "titles": {},
            "full_texts": {}
        }
        for token, docs in self.index_data.items():
            data_to_save[token] = {doc_id: tfidf for doc_id, tfidf in docs.items()}

        data_to_save["titles"] = self.doc_titles
        data_to_save["full_texts"] = self.doc_fulltext

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
        self.doc_fulltext.clear()

        tokens = loaded.get("tokens", {})
        for token, docs in tokens.items():
            self.index_data[token] = docs
        self.doc_titles = loaded.get("titles", {})
        self.doc_fulltext = loaded.get("full_texts", {})