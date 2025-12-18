# AI Features Summary - Gemini Integration

## Overview
This document summarizes all AI features implemented using Google Gemini API in the Soutenance Manager application.

## Implemented AI Features

### 1. Student Dashboard - Automatic Thesis Analysis
**Location**: `backend/app/services/ai.py`
**Endpoints**: `/api/students/soutenance-requests/`

When a student submits a thesis defense request with a PDF report:
- **Automatic Summary**: AI generates a concise summary of the thesis
- **Domain Classification**: AI identifies the thesis domain (e.g., "Artificial Intelligence", "Web Development")
- **Similarity Scoring**: AI calculates a similarity score between title and content

**Features**:
- Uses Gemini 2.0 Flash Experimental model (fast, efficient)
- Automatic fallback to Gemini Flash 1.5 on rate limits
- Logging with ✅/⚠️/❌ indicators for monitoring
- Graceful degradation with 85% confidence when AI unavailable

**Code Example**:
```python
from app.services.ai import summarize, classify_domain, similarity_score

# These functions are called automatically during thesis submission
summary = summarize(pdf_text)  # Returns 2-3 sentence summary
domain = classify_domain(thesis_title, pdf_text)  # Returns domain classification
score = similarity_score(thesis_title, pdf_text)  # Returns 0-100 score
```

### 2. Manager Dashboard - AI Jury Recommendations
**Location**: `backend/app/services/jury_ai.py`
**Endpoints**: `/api/defenses/{defense_id}/jury-suggestions`

When a manager schedules a defense, AI suggests the best jury members:
- **Smart Matching**: AI analyzes thesis domain and matches with professor specialties
- **Reasoning**: Each suggestion includes AI-generated explanation
- **Fallback Logic**: Uses keyword matching when Gemini quota exceeded

**Features**:
- Analyzes thesis title, domain, and professor specialties
- Returns top 3 recommended professors with reasons
- Integrated into schedule defense sheet with beautiful UI
- One-click "Add" button to select suggested professors

**API Response Example**:
```json
[
  {
    "professor_id": 5,
    "name": "Ahmed Alami",
    "reason": "Specialty match: Artificial Intelligence & Machine Learning"
  },
  {
    "professor_id": 6,
    "name": "Fatima Bennani",
    "reason": "Specialty match: Web Development & Cloud Computing"
  }
]
```

**Frontend Integration**:
- AI suggestions displayed in blue card above professor selector
- Shows emoji 🤖 to indicate AI-powered recommendations
- Each suggestion shows professor name and reasoning
- Quick "Add" button to select recommended professors

## Technical Architecture

### AI Service Layer
```
backend/app/services/
├── ai.py           # Core Gemini integration for thesis analysis
└── jury_ai.py      # Jury recommendation system
```

### API Layer
```
backend/app/api/
├── student.py              # Student thesis submission (uses ai.py)
└── thesis_defense.py       # Jury suggestions endpoint
```

### Frontend Integration
```
frontend/
├── services/api.ts         # API client with getJurySuggestions()
└── components/
    └── schedule-defense-sheet.tsx  # UI for AI jury suggestions
```

## Configuration

### Environment Variables
Add to `backend/.env`:
```bash
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
```

### Rate Limits (Gemini Free Tier)
- **Model**: gemini-2.0-flash-exp
- **Fallback**: gemini-1.5-flash
- **Free tier limits**: 15 RPM, 1 million TPM
- **Automatic fallback**: System switches to fallback model on quota errors

## Testing

### Test Jury Suggestions
```bash
# Get AI recommendations for defense ID 13
curl http://localhost:8000/api/defenses/13/jury-suggestions
```

### Check Backend Logs
```bash
# View AI service logs
docker compose logs backend --tail=50

# Look for indicators:
# ✅ = Success
# ⚠️ = Fallback used
# ❌ = Error (still works with fallback logic)
```

## Database Schema

### professors Table
```sql
CREATE TABLE professors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    specialty VARCHAR(255)  -- Used by AI for matching
);
```

### Test Data
3 professors added with specialties:
1. Ahmed Alami - "Artificial Intelligence & Machine Learning"
2. Fatima Bennani - "Web Development & Cloud Computing"
3. Mohamed El Idrissi - "IoT & Embedded Systems"

## Future AI Features (Planned)

### Manager Dashboard
- [ ] Report quality analysis
- [ ] Plagiarism detection alerts
- [ ] Automatic scheduling conflict detection

### Professor Dashboard
- [ ] AI-generated evaluation hints
- [ ] Key points extraction from thesis reports
- [ ] Evaluation rubric suggestions

## Code Quality

### Logging
All AI operations include detailed logging:
```python
print(f"✅ GEMINI SUCCESS - Summary generated: {summary[:50]}...")
print(f"⚠️ GEMINI FALLBACK - Using fallback model due to rate limit")
print(f"❌ GEMINI FAILED - Error: {str(e)}")
```

### Error Handling
- Graceful degradation on API failures
- Fallback values with realistic confidence scores
- No crashes - system continues working even without AI

### Performance
- Fast response times with Flash models
- Efficient PDF text extraction
- Caching potential for repeated queries

## Deployment Notes

1. **API Key Security**: Store GEMINI_API_KEY in environment variables, never commit to git
2. **Rate Limiting**: Monitor usage at https://ai.dev/usage?tab=rate-limit
3. **Model Selection**: Use flash models for production (faster, cheaper)
4. **Fallback Strategy**: Always implement fallback logic for production reliability

## Credits
- **AI Model**: Google Gemini 2.0 Flash Experimental
- **Integration**: Custom FastAPI + React implementation
- **Team**: Khalid (AI integration), Team members (frontend/backend)
