from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import os
import torch
from typing import Optional, List

# Check if GPU is available
device = 0 if torch.cuda.is_available() else -1

# Model name
MODEL_NAME = "t5-small"  # Alternative: "google/pegasus-xsum"

# Cache directory for models
MODELS_DIR = "models"
os.makedirs(MODELS_DIR, exist_ok=True)

# Initialize summarization pipeline
summarizer = None

def load_summarizer():
    """
    Load the summarization model
    """
    global summarizer
    
    if summarizer is None:
        try:
            # Load tokenizer and model
            print(f"Loading summarization model: {MODEL_NAME}")
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=MODELS_DIR)
            model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, cache_dir=MODELS_DIR)
            
            # Create summarization pipeline
            summarizer = pipeline(
                "summarization",
                model=model,
                tokenizer=tokenizer,
                device=device
            )
            
            print(f"Successfully loaded summarization model: {MODEL_NAME}")
        except Exception as e:
            print(f"Error loading summarization model: {str(e)}")
            # Fallback to a simple extractive summarization
            summarizer = None

def chunk_text(text: str, max_length: int = 1024) -> List[str]:
    """
    Split text into chunks that fit within the model's max input length
    
    Args:
        text: The text to chunk
        max_length: Maximum chunk length in characters
        
    Returns:
        List of text chunks
    """
    # Split text into sentences
    sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # If adding this sentence would exceed max_length, start a new chunk
        if len(current_chunk) + len(sentence) + 1 > max_length and current_chunk:
            chunks.append(current_chunk)
            current_chunk = sentence + "."
        else:
            current_chunk += sentence + "."
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def generate_summary(text: str, max_length: int = 150, min_length: int = 40) -> str:
    """
    Generate a summary of the text using a pre-trained model
    
    Args:
        text: The text to summarize
        max_length: Maximum summary length in tokens
        min_length: Minimum summary length in tokens
        
    Returns:
        Generated summary
    """
    # Load summarizer if not already loaded
    if summarizer is None:
        load_summarizer()
    
    # If text is too short, return it as is
    if len(text.split()) < min_length:
        return text
    
    try:
        if summarizer:
            # Chunk text if it's too long
            if len(text) > 1024:
                chunks = chunk_text(text)
                chunk_summaries = []
                
                for chunk in chunks:
                    try:
                        # Generate summary for each chunk
                        summary = summarizer(
                            chunk,
                            max_length=max_length // len(chunks),
                            min_length=min_length // len(chunks),
                            do_sample=False
                        )
                        chunk_summaries.append(summary[0]['summary_text'])
                    except Exception as chunk_error:
                        print(f"Error summarizing chunk: {str(chunk_error)}")
                        # Use first few sentences as fallback
                        chunk_summaries.append(extractive_summary(chunk, sentences=1))
                
                # Combine chunk summaries
                combined_summary = " ".join(chunk_summaries)
                
                # If combined summary is still too long, summarize it again
                if len(combined_summary.split()) > max_length:
                    try:
                        final_summary = summarizer(
                            combined_summary,
                            max_length=max_length,
                            min_length=min_length,
                            do_sample=False
                        )
                        return final_summary[0]['summary_text']
                    except Exception as final_error:
                        print(f"Error generating final summary: {str(final_error)}")
                        return extractive_summary(combined_summary, sentences=3)
                
                return combined_summary
            else:
                # Generate summary directly
                try:
                    summary = summarizer(
                        text,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False
                    )
                    return summary[0]['summary_text']
                except Exception as direct_error:
                    print(f"Error generating direct summary: {str(direct_error)}")
                    return extractive_summary(text, sentences=3)
        else:
            # Fallback to a simple extractive summary
            print("Using extractive summary fallback")
            return extractive_summary(text, sentences=3)
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        return extractive_summary(text, sentences=3)

def extractive_summary(text: str, sentences: int = 3) -> str:
    """
    Generate a simple extractive summary by selecting the first few sentences
    
    Args:
        text: The text to summarize
        sentences: Number of sentences to include
        
    Returns:
        Extractive summary
    """
    # Split text into sentences
    text_sentences = [s.strip() for s in text.replace('\n', ' ').split('.') if s.strip()]
    
    # Select the first few sentences
    summary_sentences = text_sentences[:sentences]
    
    # Join sentences into a summary
    summary = ". ".join(summary_sentences)
    if not summary.endswith("."):
        summary += "."
    
    return summary