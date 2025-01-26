import spacy

class Tokenizer:
    """
    Minimal spaCy pipeline: only 'tagger' + 'attribute_ruler' for lemma,
    chunking if text is big, ignoring parser/ner for speed.
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        self.nlp.max_length = 200_000  # Just in case
        self.CHUNK_SIZE = 50_000       # We'll chunk text in 50K increments

    def tokenize(self, text):
        tokens = []
        # chunk if needed
        for start in range(0, len(text), self.CHUNK_SIZE):
            chunk = text[start : start + self.CHUNK_SIZE]
            doc = self.nlp(chunk)
            for token in doc:
                # skip punctuation, digits, stops, etc.
                if not token.is_alpha:
                    continue
                if token.is_stop:
                    continue
                tokens.append(token.lemma_.lower())
        return tokens
