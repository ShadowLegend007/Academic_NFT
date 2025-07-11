from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import numpy as np
from typing import List, Tuple, Dict, Any
from utils.plagiarism_algorithms import PlagiarismDetector

# Directory containing reference documents
# Update the corpus directory path to be relative to the backend directory
CORPUS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "corpus")
print(f"Corpus directory path: {CORPUS_DIR}")

def load_corpus() -> List[str]:
    """
    Load reference documents from the corpus directory
    
    Returns:
        List of document texts
    """
    corpus = []
    
    # Check if corpus directory exists
    if not os.path.exists(CORPUS_DIR):
        print(f"Corpus directory not found at {CORPUS_DIR}. Creating directory.")
        os.makedirs(CORPUS_DIR, exist_ok=True)
        # Create a sample document if corpus is empty
        with open(os.path.join(CORPUS_DIR, "sample.txt"), "w") as f:
            f.write("This is a sample document for plagiarism detection.")
            print("Created sample document in corpus directory.")
    
    # List all files in the corpus directory
    try:
        files = os.listdir(CORPUS_DIR)
        print(f"Found {len(files)} files in corpus directory: {files}")
    except Exception as e:
        print(f"Error listing corpus directory: {str(e)}")
        files = []
    
    # Load all documents from corpus directory
    for filename in files:
        if filename.endswith(".txt"):
            file_path = os.path.join(CORPUS_DIR, filename)
            print(f"Loading corpus file: {file_path}")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        content = f.read()
                        corpus.append(content)
                        print(f"Successfully loaded {filename}, length: {len(content)} characters")
                    except UnicodeDecodeError:
                        # Try with a different encoding if UTF-8 fails
                        with open(file_path, "r", encoding="latin-1") as f2:
                            content = f2.read()
                            corpus.append(content)
                            print(f"Loaded {filename} with latin-1 encoding, length: {len(content)} characters")
            except Exception as e:
                print(f"Error reading corpus file {filename}: {str(e)}")
    
    print(f"Loaded {len(corpus)} documents into corpus")
    return corpus

def check_plagiarism(text: str) -> float:
    """
    Check document for plagiarism against corpus using multiple algorithms
    
    Args:
        text: The document text to check
        
    Returns:
        Plagiarism score between 0 and 1
    """
    try:
        print("Starting comprehensive plagiarism check...")
        
        # Initialize the plagiarism detector
        detector = PlagiarismDetector()
        
        # Load corpus
        corpus = load_corpus()
        
        # Use comprehensive plagiarism detection
        results = detector.check_plagiarism_comprehensive(text, corpus)
        
        print(f"Comprehensive plagiarism check complete:")
        print(f"  - Cosine similarity: {results['cosine_similarity']:.4f}")
        print(f"  - File similarity: {results['file_similarity']:.2f}%")
        print(f"  - N-gram similarity: {results['ngram_similarity']:.2f}%")
        print(f"  - Overall score: {results['overall_score']:.4f}")
        
        if results['similar_passages']:
            print(f"  - Found {len(results['similar_passages'])} similar passages")
        
        return results['overall_score']
        
    except Exception as e:
        print(f"Error in plagiarism check: {str(e)}")
        return 0.0

def get_similar_passages(text: str, threshold: float = 0.7) -> List[Dict[str, Any]]:
    """
    Find similar passages between the document and corpus
    
    Args:
        text: The document text to check
        threshold: Similarity threshold (0-1)
        
    Returns:
        List of similar passages with similarity scores
    """
    try:
        print(f"Finding similar passages with threshold {threshold}...")
        
        # Load corpus
        corpus = load_corpus()
        
        try:
            corpus_files = [f for f in os.listdir(CORPUS_DIR) if f.endswith(".txt")]
            print(f"Found {len(corpus_files)} corpus files")
        except Exception as e:
            print(f"Error listing corpus files: {str(e)}")
            corpus_files = ["unknown.txt"] * len(corpus)
        
        # Split document into paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        print(f"Document split into {len(paragraphs)} paragraphs")
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        
        similar_passages = []
        
        # Check each paragraph against corpus
        for i, paragraph in enumerate(paragraphs):
            # Skip very short paragraphs
            if len(paragraph.split()) < 10:
                continue
            
            # For each corpus document
            for j, doc in enumerate(corpus):
                # Split corpus document into paragraphs
                corpus_paragraphs = [p.strip() for p in doc.split("\n\n") if p.strip()]
                
                # Check paragraph against each corpus paragraph
                for k, corpus_paragraph in enumerate(corpus_paragraphs):
                    # Skip very short paragraphs
                    if len(corpus_paragraph.split()) < 10:
                        continue
                    
                    # Compute TF-IDF and similarity
                    try:
                        tfidf = vectorizer.fit_transform([paragraph, corpus_paragraph])
                        similarity = cosine_similarity(tfidf[0], tfidf[1])[0][0]
                        
                        # If similarity above threshold, add to results
                        if similarity >= threshold:
                            similar_passages.append({
                                "document_paragraph": paragraph,
                                "corpus_paragraph": corpus_paragraph,
                                "corpus_file": corpus_files[j] if j < len(corpus_files) else "unknown.txt",
                                "similarity": float(similarity)
                            })
                            print(f"Found similar passage with similarity {similarity:.4f}")
                    except Exception as e:
                        print(f"Error comparing paragraphs: {str(e)}")
                        continue
        
        # Sort by similarity (highest first)
        similar_passages.sort(key=lambda x: x["similarity"], reverse=True)
        print(f"Found {len(similar_passages)} similar passages above threshold {threshold}")
        
        return similar_passages
        
    except Exception as e:
        print(f"Error finding similar passages: {str(e)}")
        return []