import nltk

def setup_nltk():
    """
    Download required NLTK resources.
    Ensures the lemmatizer and tokenizer work without manual intervention.
    """
    try:
        print("Setting up NLTK...")
        nltk.download("punkt")  # Tokenizer models
        nltk.download("wordnet")  # Lemmatizer models
        nltk.download("omw-1.4")  # Lemmatizer's wordnet data
        print("NLTK setup complete!")
    except Exception as e:
        print(f"Error during NLTK setup: {e}")