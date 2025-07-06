#!/usr/bin/env python3
"""
Test script for the enhanced plagiarism detection algorithms
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.plagiarism_algorithms import PlagiarismDetector, CosineSimilarity, FileSimilarity, NGramSimilarity

def test_cosine_similarity():
    """Test cosine similarity algorithm"""
    print("Testing Cosine Similarity...")
    
    text1 = "The quick brown fox jumps over the lazy dog."
    text2 = "A quick brown fox jumps over a lazy dog."
    text3 = "The weather is beautiful today."
    
    # Test similar texts
    similarity1 = CosineSimilarity.cosine_sim(text1, text2)
    print(f"Similarity between similar texts: {similarity1:.4f}")
    
    # Test different texts
    similarity2 = CosineSimilarity.cosine_sim(text1, text3)
    print(f"Similarity between different texts: {similarity2:.4f}")
    
    assert similarity1 > similarity2, "Similar texts should have higher similarity"
    print("✓ Cosine similarity test passed\n")

def test_file_similarity():
    """Test file similarity algorithm"""
    print("Testing File Similarity...")
    
    text1 = "The quick brown fox jumps over the lazy dog. This is a sample text for testing."
    text2 = "A quick brown fox jumps over a lazy dog. This is another sample text for testing."
    text3 = "The weather is beautiful today. I love going for walks in the park."
    
    # Test similar texts
    similarity1 = FileSimilarity.find_file_similarity(text1, text2)
    print(f"File similarity between similar texts: {similarity1:.2f}%")
    
    # Test different texts
    similarity2 = FileSimilarity.find_file_similarity(text1, text3)
    print(f"File similarity between different texts: {similarity2:.2f}%")
    
    assert similarity1 > similarity2, "Similar texts should have higher file similarity"
    print("✓ File similarity test passed\n")

def test_ngram_similarity():
    """Test n-gram similarity algorithm"""
    print("Testing N-Gram Similarity...")
    
    text1 = "The quick brown fox jumps over the lazy dog. This is a sample text for testing plagiarism detection algorithms."
    text2 = "A quick brown fox jumps over a lazy dog. This is another sample text for testing plagiarism detection algorithms."
    
    # Test n-gram generation
    queries = NGramSimilarity.get_queries(text1, 5)
    print(f"Generated {len(queries)} n-gram queries")
    
    # Test similarity calculation
    similarity, links = NGramSimilarity.find_similarity(text1)
    print(f"N-gram similarity score: {similarity:.2f}%")
    
    print("✓ N-gram similarity test passed\n")

def test_comprehensive_detector():
    """Test the comprehensive plagiarism detector"""
    print("Testing Comprehensive Plagiarism Detector...")
    
    detector = PlagiarismDetector()
    
    # Test text
    test_text = "The quick brown fox jumps over the lazy dog. This is a sample text for testing plagiarism detection algorithms."
    
    # Reference texts
    reference_texts = [
        "A quick brown fox jumps over a lazy dog. This is another sample text for testing.",
        "The weather is beautiful today. I love going for walks in the park.",
        "Machine learning algorithms are used for pattern recognition and data analysis."
    ]
    
    # Test comprehensive analysis
    results = detector.check_plagiarism_comprehensive(test_text, reference_texts)
    
    print(f"Comprehensive analysis results:")
    print(f"  - Cosine similarity: {results['cosine_similarity']:.4f}")
    print(f"  - File similarity: {results['file_similarity']:.2f}%")
    print(f"  - N-gram similarity: {results['ngram_similarity']:.2f}%")
    print(f"  - Overall score: {results['overall_score']:.4f}")
    print(f"  - Similar passages found: {len(results['similar_passages'])}")
    
    # Test two-text comparison
    comparison = detector.compare_two_texts(test_text, reference_texts[0])
    print(f"Two-text comparison:")
    print(f"  - Cosine similarity: {comparison['cosine_similarity']:.4f}")
    print(f"  - File similarity: {comparison['file_similarity']:.2f}%")
    
    print("✓ Comprehensive detector test passed\n")

def test_edge_cases():
    """Test edge cases"""
    print("Testing Edge Cases...")
    
    detector = PlagiarismDetector()
    
    # Test empty text
    empty_results = detector.check_plagiarism_comprehensive("", ["some reference text"])
    print(f"Empty text analysis: {empty_results['overall_score']:.4f}")
    
    # Test very short text
    short_results = detector.check_plagiarism_comprehensive("Hello world", ["Hello world"])
    print(f"Short text analysis: {short_results['overall_score']:.4f}")
    
    # Test with no reference texts
    no_ref_results = detector.check_plagiarism_comprehensive("Some text to analyze")
    print(f"No reference texts analysis: {no_ref_results['overall_score']:.4f}")
    
    print("✓ Edge cases test passed\n")

def main():
    """Run all tests"""
    print("=" * 60)
    print("PLAGIARISM DETECTION ALGORITHMS TEST SUITE")
    print("=" * 60)
    
    try:
        test_cosine_similarity()
        test_file_similarity()
        test_ngram_similarity()
        test_comprehensive_detector()
        test_edge_cases()
        
        print("=" * 60)
        print("ALL TESTS PASSED! ✅")
        print("=" * 60)
        print("\nThe plagiarism detection algorithms have been successfully implemented.")
        print("You can now use the enhanced API endpoints:")
        print("  - POST /api/v1/analyze-text")
        print("  - POST /api/v1/compare-texts")
        print("  - POST /api/v1/analyze-detailed")
        print("  - GET /api/v1/corpus-info")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 