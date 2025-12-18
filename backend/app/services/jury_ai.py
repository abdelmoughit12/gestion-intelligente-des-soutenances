"""AI-powered jury recommendation system."""

from typing import List, Dict
import os
import logging

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = logging.getLogger(__name__)


def suggest_jury_members(
    thesis_title: str,
    thesis_domain: str | Dict,
    available_professors: List[Dict],
    num_suggestions: int = 3
) -> List[Dict]:
    """
    Use Gemini AI to recommend the best jury members based on thesis domain and professor specialties.
    
    Args:
        thesis_title: Title of the thesis
        thesis_domain: Domain classification (string or dict with confidences)
        available_professors: List of {id, name, specialty} dicts
        num_suggestions: Number of professors to recommend
        
    Returns:
        List of recommended professors with reasoning
    """
    if not available_professors:
        return []
    
    # Fallback: simple keyword matching
    fallback_suggestions = _fallback_jury_matching(thesis_domain, available_professors, num_suggestions)
    
    # Try Gemini AI
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not genai:
        logger.warning("⚠️ GEMINI UNAVAILABLE - Using keyword-based jury suggestions")
        return fallback_suggestions
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        
        # Parse domain if it's a JSON string
        domain_text = thesis_domain
        if isinstance(thesis_domain, dict):
            domain_text = ", ".join([f"{k} ({v*100:.0f}%)" for k, v in sorted(thesis_domain.items(), key=lambda x: x[1], reverse=True)])
        
        # Build professor list
        prof_list = "\n".join([f"- ID {p['id']}: {p['name']} (Specialty: {p.get('specialty', 'General')})" for p in available_professors])
        
        prompt = f"""You are an academic committee organizer. Recommend the best {num_suggestions} professors for a thesis defense jury.

Thesis Title: {thesis_title}
Thesis Domain: {domain_text}

Available Professors:
{prof_list}

Select the {num_suggestions} most suitable professors based on domain expertise match. Return ONLY a JSON array:
[
  {{"professor_id": 5, "name": "Ahmed Alami", "reason": "Expert in AI, perfect match for thesis domain"}},
  ...
]

JSON response:"""
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Extract JSON
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()
        
        import json
        suggestions = json.loads(text)
        
        logger.info(f"✅ GEMINI SUCCESS - Generated {len(suggestions)} jury recommendations")
        return suggestions[:num_suggestions]
        
    except Exception as e:
        logger.error(f"❌ GEMINI FAILED - Jury recommendation error: {e}")
        return fallback_suggestions


def _fallback_jury_matching(domain, professors: List[Dict], num: int) -> List[Dict]:
    """Simple keyword-based matching as fallback."""
    domain_str = str(domain).lower()
    
    scored_profs = []
    for prof in professors:
        specialty = prof.get('specialty', '').lower()
        score = 0
        
        # Simple keyword matching
        keywords = domain_str.split()
        for keyword in keywords:
            if keyword in specialty or specialty in keyword:
                score += 1
        
        scored_profs.append({
            "professor_id": prof['id'],
            "name": prof['name'],
            "reason": f"Specialty match: {prof.get('specialty', 'General')}",
            "score": score
        })
    
    # Sort by score and return top N
    scored_profs.sort(key=lambda x: x['score'], reverse=True)
    return [{"professor_id": p["professor_id"], "name": p["name"], "reason": p["reason"]} 
            for p in scored_profs[:num]]
