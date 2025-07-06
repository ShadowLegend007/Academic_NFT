import re
import math
from collections import Counter
from nltk.corpus import stopwords
import nltk
from typing import Dict, List, Tuple, Any
import os

# Download NLTK data if not already downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Regular expression for word matching
WORD = re.compile(r'\w+')

class CosineSimilarity:
    """Cosine similarity implementation for text comparison"""
    
    @staticmethod
    def get_cosine(vec1: Dict[str, int], vec2: Dict[str, int]) -> float:
        """
        Calculate cosine similarity between two vectors
        
        Args:
            vec1: First vector (word frequency dictionary)
            vec2: Second vector (word frequency dictionary)
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        intersection = set(vec1.keys()) & set(vec2.keys())
        
        # Find matching words with minimum frequency
        match_words = {}
        for word in intersection:
            match_words[word] = min(vec1[word], vec2[word])
        
        # Calculate numerator
        numerator = sum([vec1[x] * match_words[x] for x in intersection])
        
        # Calculate denominator
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([match_words[x]**2 for x in match_words.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        # Check for divide by zero
        if denominator == 0:
            return 0.0
        else:
            return float(numerator) / denominator
    
    @staticmethod
    def text_to_vector(text: str) -> Dict[str, int]:
        """
        Convert text to word frequency vector
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with words as keys and frequencies as values
        """
        words = WORD.findall(text)
        return Counter(words)
    
    @staticmethod
    def cosine_sim(text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        t1 = text1.lower()
        t2 = text2.lower()
        
        vector1 = CosineSimilarity.text_to_vector(t1)
        vector2 = CosineSimilarity.text_to_vector(t2)
        
        return CosineSimilarity.get_cosine(vector1, vector2)

class FileSimilarity:
    """File similarity implementation using TF-IDF approach"""
    
    @staticmethod
    def find_file_similarity(input_query: str, database: str) -> float:
        """
        Calculate similarity between input text and database text using TF-IDF
        
        Args:
            input_query: Input text to check
            database: Reference text to compare against
            
        Returns:
            Similarity percentage (0-100)
        """
        universal_set_of_unique_words = []
        match_percentage = 0
        
        lowercase_query = input_query.lower()
        en_stops = set(stopwords.words('english'))
        
        # Replace punctuation by space and split
        query_word_list = re.sub(r"[^\w]", " ", lowercase_query).split()
        
        # Add unique words from query
        for word in query_word_list:
            if word not in universal_set_of_unique_words:
                universal_set_of_unique_words.append(word)
        
        database_lower = database.lower()
        
        # Replace punctuation by space and split
        database_word_list = re.sub(r"[^\w]", " ", database_lower).split()
        
        # Add unique words from database
        for word in database_word_list:
            if word not in universal_set_of_unique_words:
                universal_set_of_unique_words.append(word)
        
        # Remove stop words
        for word in universal_set_of_unique_words[:]:  # Use slice to avoid modification during iteration
            if word in en_stops:
                universal_set_of_unique_words.remove(word)
        
        # Calculate TF (Term Frequency) for both texts
        query_tf = []
        database_tf = []
        
        for word in universal_set_of_unique_words:
            query_tf_counter = 0
            database_tf_counter = 0
            
            # Count word frequency in query
            for word2 in query_word_list:
                if word == word2:
                    query_tf_counter += 1
            query_tf.append(query_tf_counter)
            
            # Count word frequency in database
            for word2 in database_word_list:
                if word == word2:
                    database_tf_counter += 1
            database_tf.append(database_tf_counter)
        
        # Calculate dot product
        dot_product = 0
        for i in range(len(query_tf)):
            dot_product += query_tf[i] * database_tf[i]
        
        # Calculate vector magnitudes
        query_vector_magnitude = 0
        for i in range(len(query_tf)):
            query_vector_magnitude += query_tf[i]**2
        query_vector_magnitude = math.sqrt(query_vector_magnitude)
        
        database_vector_magnitude = 0
        for i in range(len(database_tf)):
            database_vector_magnitude += database_tf[i]**2
        database_vector_magnitude = math.sqrt(database_vector_magnitude)
        
        # Calculate similarity percentage
        if query_vector_magnitude * database_vector_magnitude == 0:
            return 0.0
        
        match_percentage = (float(dot_product) / (query_vector_magnitude * database_vector_magnitude)) * 100
        
        return match_percentage

class NGramSimilarity:
    """N-gram based similarity for web search and advanced plagiarism detection"""
    
    @staticmethod
    def get_queries(text: str, n: int) -> List[List[str]]:
        """
        Generate n-gram queries from text
        
        Args:
            text: Input text
            n: N-gram size
            
        Returns:
            List of n-gram queries
        """
        sentence_enders = re.compile("['.!?]")
        sentence_list = sentence_enders.split(text)
        sentence_splits = []
        en_stops = set(stopwords.words('english'))
        
        # Process each sentence
        for sentence in sentence_list:
            x = re.compile(r'\W+', re.UNICODE).split(sentence)
            # Remove stop words
            x = [word for word in x if word.lower() not in en_stops and word != '']
            sentence_splits.append(x)
        
        final_queries = []
        
        # Generate n-grams from sentences
        for sentence in sentence_splits:
            l = len(sentence)
            if l > n:
                l = int(l/n)
                index = 0
                for i in range(0, l):
                    final_queries.append(sentence[index:index+n])
                    index = index + n - 1
                    if index + n > l:
                        index = l - n - 1
                if index != len(sentence):
                    final_queries.append(sentence[len(sentence)-index:len(sentence)])
            else:
                if l > 4:
                    final_queries.append(sentence)
        
        return final_queries
    
    @staticmethod
    def find_similarity(text: str, n: int = 9) -> Tuple[float, Dict[str, float]]:
        """
        Find similarity using n-gram approach (simplified version without web search)
        
        Args:
            text: Input text
            n: N-gram size (default: 9)
            
        Returns:
            Tuple of (total_percentage, output_links)
        """
        queries = NGramSimilarity.get_queries(text, n)
        print('GetQueries task complete')
        
        q = [' '.join(d) for d in queries]
        
        # Remove empty queries
        while "" in q:
            q.remove("")
        
        count = len(q)
        if count > 100:
            count = 100
        
        # For now, return a simplified similarity score
        # In a full implementation, this would integrate with web search
        total_percent = 0.0
        output_links = {}
        
        # Calculate basic similarity based on query complexity
        if count > 0:
            # Simple heuristic: more complex queries might indicate more original content
            total_percent = min(100.0, max(0.0, (100 - count * 0.5)))
        
        return total_percent, output_links

class PlagiarismDetector:
    """Main plagiarism detection class that combines all algorithms"""
    
    def __init__(self):
        self.cosine_sim = CosineSimilarity()
        self.file_sim = FileSimilarity()
        self.ngram_sim = NGramSimilarity()
    
    def check_plagiarism_comprehensive(self, text: str, reference_texts: List[str] = None) -> Dict[str, Any]:
        """
        Comprehensive plagiarism check using multiple algorithms
        
        Args:
            text: Text to check for plagiarism
            reference_texts: List of reference texts to compare against
            
        Returns:
            Dictionary with plagiarism scores and details
        """
        results = {
            "cosine_similarity": 0.0,
            "file_similarity": 0.0,
            "ngram_similarity": 0.0,
            "overall_score": 0.0,
            "similar_passages": [],
            "details": {}
        }
        
        if not reference_texts:
            # Use default corpus or return basic analysis
            results["ngram_similarity"], _ = self.ngram_sim.find_similarity(text)
            results["overall_score"] = results["ngram_similarity"] / 100.0
            return results
        
        # Calculate cosine similarity with each reference text
        cosine_scores = []
        file_scores = []
        
        for i, ref_text in enumerate(reference_texts):
            # Cosine similarity
            cosine_score = self.cosine_sim.cosine_sim(text, ref_text)
            cosine_scores.append(cosine_score)
            
            # File similarity
            file_score = self.file_sim.find_file_similarity(text, ref_text)
            file_scores.append(file_score)
            
            # Add similar passages if similarity is high
            if cosine_score > 0.7:
                results["similar_passages"].append({
                    "reference_index": i,
                    "cosine_similarity": cosine_score,
                    "file_similarity": file_score,
                    "reference_preview": ref_text[:200] + "..." if len(ref_text) > 200 else ref_text
                })
        
        # Calculate average scores
        if cosine_scores:
            results["cosine_similarity"] = max(cosine_scores)
        if file_scores:
            results["file_similarity"] = max(file_scores)
        
        # N-gram similarity
        ngram_score, _ = self.ngram_sim.find_similarity(text)
        results["ngram_similarity"] = ngram_score
        
        # Calculate overall score (weighted average)
        weights = {
            "cosine": 0.4,
            "file": 0.4,
            "ngram": 0.2
        }
        
        overall_score = (
            results["cosine_similarity"] * weights["cosine"] +
            (results["file_similarity"] / 100.0) * weights["file"] +
            (results["ngram_similarity"] / 100.0) * weights["ngram"]
        )
        
        results["overall_score"] = min(1.0, overall_score)
        results["details"] = {
            "cosine_scores": cosine_scores,
            "file_scores": file_scores,
            "weights": weights
        }
        
        return results
    
    def compare_two_texts(self, text1: str, text2: str) -> Dict[str, float]:
        """
        Compare two texts directly
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Dictionary with similarity scores
        """
        return {
            "cosine_similarity": self.cosine_sim.cosine_sim(text1, text2),
            "file_similarity": self.file_sim.find_file_similarity(text1, text2)
        } 