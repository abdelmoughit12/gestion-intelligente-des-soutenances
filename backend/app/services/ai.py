"""Lightweight Gemini integration with safe fallbacks.

- Uses GEMINI_API_KEY if provided; otherwise returns heuristic defaults.
- Designed for Khalid's student upload flow (summary, domain, similarity).
- Does not handle authentication; caller must provide inputs.
"""

from __future__ import annotations

import os
import json
from typing import List, Optional, Dict
from pathlib import Path

try:
    import google.generativeai as genai  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    genai = None  # type: ignore

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None


def _get_model(prefer_lite: bool = False) -> Optional[object]:
    """Get Gemini model, trying Flash first then Flash-Lite on rate limits."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or genai is None:
        return None
    try:
        genai.configure(api_key=api_key)
        model_name = "gemini-2.5-flash-lite" if prefer_lite else "gemini-2.5-flash"
        return genai.GenerativeModel(model_name)
    except Exception:
        return None


def _generate_with_fallback(model, prompt: str) -> Optional[str]:
    """Generate content with automatic fallback to Flash-Lite on rate limit."""
    if not model:
        return None
    
    try:
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", None)
        if text:
            return text.strip()
    except Exception as e:
        error_str = str(e)
        # Check if it's a rate limit error (429)
        if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
            # Try Flash-Lite model
            try:
                lite_model = _get_model(prefer_lite=True)
                if lite_model and lite_model != model:
                    resp = lite_model.generate_content(prompt)
                    text = getattr(resp, "text", None)
                    if text:
                        return text.strip()
            except Exception:
                pass
    
    return None


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from PDF using multiple methods for best accuracy."""
    text = ""
    
    # Try pdfplumber first (most accurate)
    if pdfplumber:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text.strip()
        except Exception:
            pass
    
    # Fallback to PyPDF2
    if PyPDF2:
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                return text.strip()
        except Exception:
            pass
    
    return text.strip() or "[Unable to extract text from PDF]"


def summarize(title: str, pdf_path: str | None = None) -> str:
    """Generate English summary from PDF content."""
    fallback = f"Auto-generated summary placeholder for '{title}'. AI module will replace this text."
    model = _get_model()
    if not model:
        return fallback
    
    # Extract PDF content if path provided
    content = ""
    if pdf_path and Path(pdf_path).exists():
        content = extract_pdf_text(pdf_path)
        # Limit to first 8000 chars to avoid token limits
        if len(content) > 8000:
            content = content[:8000] + "..."
    
    if not content or content == "[Unable to extract text from PDF]":
        content = f"Title: {title}"
    
    prompt = (
        "You are an academic assistant. Write a concise 2-3 sentence summary of this thesis/research paper in English.\n"
        "Focus on the main research problem, methodology, and expected outcomes.\n\n"
        f"Content:\n{content}\n\n"
        "Provide only the summary, no additional commentary."
    )
    
    result = _generate_with_fallback(model, prompt)
    return result if result else fallback


def classify_domain(content: str, user_provided_domain: str, pdf_path: str | None = None) -> Dict[str, float]:
    """Classify domain with confidence percentages to verify user input.
    
    Returns dict like: {'AI': 0.7, 'Mobile': 0.2, 'Security': 0.1}
    """
    domains = ["Web", "AI", "IoT", "Mobile", "Security", "Data Science", "Other"]
    fallback = {user_provided_domain: 1.0}
    
    model = _get_model()
    if not model:
        return fallback
    
    # Extract PDF content if available
    full_content = content
    if pdf_path and Path(pdf_path).exists():
        pdf_text = extract_pdf_text(pdf_path)
        if pdf_text and pdf_text != "[Unable to extract text from PDF]":
            full_content = pdf_text[:5000]  # Limit for token efficiency
    
    prompt = (
        f"Analyze this thesis content and classify it into these domains: {', '.join(domains)}.\n"
        f"The student claims it belongs to: {user_provided_domain}\n\n"
        "Provide confidence percentages for the top 3 most relevant domains.\n"
        "Return ONLY a JSON object with domain names as keys and percentages (0-1) as values.\n"
        "Example: {\"AI\": 0.7, \"Mobile\": 0.2, \"Security\": 0.1}\n\n"
        f"Content:\n{full_content}\n\n"
        "JSON response:"
    )
    
    text = _generate_with_fallback(model, prompt)
    if text:
        try:
            # Extract JSON from response (handle markdown code blocks)
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            text = text.strip()
            result = json.loads(text)
            # Normalize and validate
            total = sum(result.values())
            if total > 0:
                return {k: round(v / total, 2) for k, v in result.items()}
        except Exception:
            pass
    
    return fallback


def similarity_score(current_content: str, previous_reports: List[Dict], pdf_path: str | None = None) -> Optional[Dict[str, any]]:
    """Calculate similarity with previous reports using semantic analysis.
    
    Returns: {'max_similarity': 0.85, 'similar_to': 'Report #123', 'method': 'gemini'}
    """
    if not previous_reports:
        return None
    
    # Extract current PDF text
    current_text = current_content
    if pdf_path and Path(pdf_path).exists():
        current_text = extract_pdf_text(pdf_path)[:3000]
    
    if not current_text or len(current_text) < 50:
        return None
    
    model = _get_model()
    if model:
        # Use Gemini for semantic similarity
        try:
            max_sim = 0.0
            similar_to = None
            
            for prev_report in previous_reports[:5]:  # Check last 5 reports
                prev_content = prev_report.get('content', prev_report.get('title', ''))
                if not prev_content or len(prev_content) < 50:
                    continue
                
                prompt = (
                    "Compare these two thesis abstracts and rate their similarity from 0.0 (completely different) to 1.0 (identical/plagiarized).\n"
                    "Consider: topic overlap, methodology, research questions, and domain.\n\n"
                    f"Current thesis:\n{current_text[:1000]}\n\n"
                    f"Previous thesis:\n{prev_content[:1000]}\n\n"
                    "Respond with ONLY a single number between 0.0 and 1.0:"
                )
                
                text = _generate_with_fallback(model, prompt)
                if text:
                    try:
                        sim = float(text)
                        if sim > max_sim:
                            max_sim = sim
                            similar_to = prev_report.get('id', 'Unknown')
                    except ValueError:
                        continue
            
            if max_sim > 0:
                return {
                    'max_similarity': round(max_sim, 2),
                    'similar_to': similar_to,
                    'method': 'gemini'
                }
        except Exception:
            pass
    
    # Fallback: Jaccard similarity with bigrams
    def get_bigrams(text: str) -> set:
        words = [w.lower() for w in text.split() if len(w) > 2]
        return set(zip(words[:-1], words[1:]))
    
    current_bigrams = get_bigrams(current_text)
    if not current_bigrams:
        return None
    
    max_sim = 0.0
    similar_to = None
    
    for prev_report in previous_reports:
        prev_content = prev_report.get('content', prev_report.get('title', ''))
        prev_bigrams = get_bigrams(prev_content)
        
        if not prev_bigrams:
            continue
        
        intersection = len(current_bigrams & prev_bigrams)
        union = len(current_bigrams | prev_bigrams)
        sim = intersection / union if union else 0.0
        
        if sim > max_sim:
            max_sim = sim
            similar_to = prev_report.get('id', 'Unknown')
    
    return {
        'max_similarity': round(max_sim, 2),
        'similar_to': similar_to,
        'method': 'jaccard'
    } if max_sim > 0 else None


# Helpers

def _heuristic_domain(text: str, fallback: str = "Other") -> str:
    keywords = {
        "ai": "AI",
        "machine": "AI",
        "deep": "AI",
        "web": "Web",
        "http": "Web",
        "mobile": "Mobile",
        "android": "Mobile",
        "ios": "Mobile",
        "iot": "IoT",
        "sensor": "IoT",
        "security": "Security",
        "encrypt": "Security",
        "data": "Data Science",
        "analytics": "Data Science",
    }
    lower = text.lower()
    for kw, domain in keywords.items():
        if kw in lower:
            return domain
    return fallback


def _normalize_domain(text: str, fallback: str) -> str:
    clean = text.strip().lower()
    mapping = {
        "web": "Web",
        "ai": "AI",
        "ia": "AI",
        "iot": "IoT",
        "mobile": "Mobile",
        "security": "Security",
        "sécurité": "Security",
        "data": "Data Science",
        "data science": "Data Science",
        "autre": "Other",
        "other": "Other",
    }
    return mapping.get(clean, fallback)
