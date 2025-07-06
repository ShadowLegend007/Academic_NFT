from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Any, List
import os
from utils.plagiarism_algorithms import PlagiarismDetector
from utils.plagiarism_check import load_corpus
from utils.summarizer import generate_summary
from utils.ipfs_upload import upload_to_ipfs
from datetime import datetime

router = APIRouter()
detector = PlagiarismDetector()

@router.post("/analyze-text")
async def analyze_text(text: str = Form(...), title: str = Form("Untitled Document")):
    """
    Analyze text for plagiarism using multiple algorithms
    """
    try:
        print(f"Analyzing text: {title}")
        
        # Load corpus for comparison
        corpus = load_corpus()
        
        # Perform comprehensive plagiarism analysis
        results = detector.check_plagiarism_comprehensive(text, corpus)
        
        # Generate summary
        summary = generate_summary(text)
        
        # Create metadata for IPFS
        metadata = {
            "title": title,
            "text": text,
            "summary": summary,
            "plagiarism_analysis": results,
            "timestamp": datetime.now().isoformat()
        }
        
        # Upload to IPFS (using text as file content)
        ipfs_cid = upload_to_ipfs(None, metadata, text_content=text)
        
        return {
            "success": True,
            "title": title,
            "summary": summary,
            "plagiarism_analysis": results,
            "ipfs_cid": ipfs_cid,
            "timestamp": metadata["timestamp"]
        }
        
    except Exception as e:
        print(f"Error in text analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/compare-texts")
async def compare_texts(text1: str = Form(...), text2: str = Form(...)):
    """
    Compare two texts directly for similarity
    """
    try:
        print("Comparing two texts...")
        
        # Compare texts using multiple algorithms
        results = detector.compare_two_texts(text1, text2)
        
        # Add additional analysis
        analysis = {
            "cosine_similarity": results["cosine_similarity"],
            "file_similarity_percentage": results["file_similarity"],
            "overall_similarity": (results["cosine_similarity"] + results["file_similarity"] / 100.0) / 2,
            "text1_length": len(text1),
            "text2_length": len(text2),
            "similarity_level": "High" if results["cosine_similarity"] > 0.7 else "Medium" if results["cosine_similarity"] > 0.4 else "Low"
        }
        
        return {
            "success": True,
            "comparison_results": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error in text comparison: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@router.post("/analyze-detailed")
async def analyze_detailed(
    text: str = Form(...),
    title: str = Form("Untitled Document"),
    include_ngram: bool = Form(True),
    include_cosine: bool = Form(True),
    include_file_similarity: bool = Form(True)
):
    """
    Detailed analysis with configurable algorithms
    """
    try:
        print(f"Performing detailed analysis: {title}")
        
        # Load corpus
        corpus = load_corpus()
        
        # Initialize results
        results = {
            "cosine_similarity": 0.0,
            "file_similarity": 0.0,
            "ngram_similarity": 0.0,
            "overall_score": 0.0,
            "similar_passages": [],
            "details": {},
            "algorithms_used": []
        }
        
        # Perform cosine similarity analysis
        if include_cosine and corpus:
            cosine_scores = []
            for i, ref_text in enumerate(corpus):
                cosine_score = detector.cosine_sim.cosine_sim(text, ref_text)
                cosine_scores.append(cosine_score)
                if cosine_score > 0.7:
                    results["similar_passages"].append({
                        "reference_index": i,
                        "cosine_similarity": cosine_score,
                        "reference_preview": ref_text[:200] + "..." if len(ref_text) > 200 else ref_text
                    })
            
            if cosine_scores:
                results["cosine_similarity"] = max(cosine_scores)
            results["algorithms_used"].append("cosine_similarity")
        
        # Perform file similarity analysis
        if include_file_similarity and corpus:
            file_scores = []
            for ref_text in corpus:
                file_score = detector.file_sim.find_file_similarity(text, ref_text)
                file_scores.append(file_score)
            
            if file_scores:
                results["file_similarity"] = max(file_scores)
            results["algorithms_used"].append("file_similarity")
        
        # Perform n-gram analysis
        if include_ngram:
            ngram_score, _ = detector.ngram_sim.find_similarity(text)
            results["ngram_similarity"] = ngram_score
            results["algorithms_used"].append("ngram_similarity")
        
        # Calculate overall score
        weights = {
            "cosine": 0.4 if include_cosine else 0,
            "file": 0.4 if include_file_similarity else 0,
            "ngram": 0.2 if include_ngram else 0
        }
        
        # Normalize weights if some algorithms are disabled
        total_weight = sum(weights.values())
        if total_weight > 0:
            for key in weights:
                weights[key] /= total_weight
        
        overall_score = (
            results["cosine_similarity"] * weights["cosine"] +
            (results["file_similarity"] / 100.0) * weights["file"] +
            (results["ngram_similarity"] / 100.0) * weights["ngram"]
        )
        
        results["overall_score"] = min(1.0, overall_score)
        results["details"]["weights"] = weights
        
        # Generate summary
        summary = generate_summary(text)
        
        return {
            "success": True,
            "title": title,
            "summary": summary,
            "plagiarism_analysis": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"Error in detailed analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Detailed analysis failed: {str(e)}")

@router.get("/corpus-info")
async def get_corpus_info():
    """
    Get information about the current corpus
    """
    try:
        corpus = load_corpus()
        
        return {
            "success": True,
            "corpus_size": len(corpus),
            "total_characters": sum(len(doc) for doc in corpus),
            "average_document_length": sum(len(doc) for doc in corpus) / len(corpus) if corpus else 0,
            "corpus_loaded": len(corpus) > 0
        }
        
    except Exception as e:
        print(f"Error getting corpus info: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get corpus info: {str(e)}")