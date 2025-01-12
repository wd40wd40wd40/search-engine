# Helper function to make snippet highlights
def snippet_highlighter(full_text: str, query: str, snippet_length: int = 30) -> str:
    words = full_text.split()
    query_lower = query.lower()

    for i, w in enumerate(words):
        if query_lower in w.lower():
            start = max(0, i - snippet_length // 2)
            end = min(len(words), i + snippet_length // 2)

            snippet_words = words[start:end]

            highlighted_snippet_words = []
            for word in snippet_words:
                if query_lower in word.lower():
                    highlighted_snippet_words.append(f"<mark>{word}</mark>")
                else:
                    highlighted_snippet_words.append(word)

            snippet = " ".join(highlighted_snippet_words)
            return snippet + "..."
        
    snippet_words = words[:snippet_length]
    return " ".join(snippet_words) + "..."
    