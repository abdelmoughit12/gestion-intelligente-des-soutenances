# API Endpoints & Critical Dependencies

## ⚠️ IMPORTANT FOR ACHRAF (Authentication Implementation)

**READ THIS BEFORE MODIFYING AUTHENTICATION OR USER MODELS!**

This document lists all endpoints and their dependencies. Many features rely on specific field names, relationships, and response structures. **Changing these without updating dependent code will break the application.**

---

## 🔴 Critical Dependencies - DO NOT BREAK

### User Model Structure
**Used by:** Student Dashboard, Professor Dashboard, Manager Dashboard, AI Services

```python
# backend/app/models/user.py
class User(Base):
    id: int                    # ⚠️ CRITICAL: Used everywhere for relationships
    email: str                 # ⚠️ CRITICAL: Used in all dashboards
    first_name: str            # ⚠️ CRITICAL: Displayed in UI tables
    last_name: str             # ⚠️ CRITICAL: Displayed in UI tables
    cni: str | None            # Optional, but must remain nullable
    role: str                  # ⚠️ CRITICAL: "student", "professor", "manager"
```

**Frontend expects these fields in:**
- `/api/professors/` response
- `/api/defenses/` response (nested in student.user)
- All dashboard APIs

### Student Model Structure
**Used by:** Student submissions, Manager dashboard, AI processing

```python
# backend/app/models/student.py
class Student(Base):
    user_id: int              # ⚠️ CRITICAL: FK to users.id
    major: str                # Displayed in manager dashboard
    cne: str                  # Student ID number
    year: int                 # Graduation year
    user: User                # ⚠️ CRITICAL: Relationship, must include user fields
```

**Frontend expects this in:**
- `/api/defenses/` response (nested as "student")
- Student dashboard API

### Professor Model Structure
**Used by:** Jury assignments, AI recommendations, Professor dashboard

```python
# backend/app/models/professor.py
class Professor(Base):
    user_id: int              # ⚠️ CRITICAL: FK to users.id
    specialty: str | None     # ⚠️ CRITICAL: Used by AI jury suggestions!
    user: User                # ⚠️ CRITICAL: Must include user.id, first_name, last_name
```

**Frontend expects this in:**
- `/api/professors/` → Returns list of professors with user data
- `/api/defenses/{id}/jury-suggestions` → AI matches specialty with thesis domain

---

## 📋 Backend API Endpoints

### Student Endpoints
**Base:** `/api/students/`

#### POST /api/students/soutenance-requests/
**Purpose:** Student submits thesis defense request with PDF  
**Request:** FormData with:
- `title`: string
- `description`: string (optional)
- `file`: PDF file

**Response:**
```json
{
  "id": 13,
  "title": "cpp project",
  "status": "pending",
  "report": {
    "file_name": "report_student_1_cpp_project_e39f84.pdf",
    "ai_summary": "...",
    "ai_domain": "{\"Other\": 0.84, ...}",
    "ai_similarity_score": 0.0
  }
}
```

**Dependencies:**
- ✅ AI service (`backend/app/services/ai.py`) for summary/domain/similarity
- ✅ Student must be authenticated (currently uses test user ID)
- ✅ Frontend: `frontend/services/api.ts` → `submitSoutenanceRequest()`

#### GET /api/students/soutenance-requests/
**Purpose:** Get all requests for current student  
**Response:** Array of thesis defenses with reports

**Dependencies:**
- ✅ Frontend: Student dashboard "My Requests" page

---

### Professor Endpoints
**Base:** `/api/professors/`

#### GET /api/professors/
**Purpose:** List all professors (used for jury selection)  
**Response:**
```json
[
  {
    "user": {
      "id": 5,
      "first_name": "Ahmed",
      "last_name": "Alami",
      "email": "ahmed.alami@example.com"
    },
    "specialty": "Artificial Intelligence & Machine Learning"
  }
]
```

**Dependencies:**
- ⚠️ CRITICAL: Manager dashboard jury selection dropdown
- ⚠️ CRITICAL: AI jury suggestions feature
- Frontend: `schedule-defense-sheet.tsx` uses this

#### GET /api/professors/assigned-soutenances
**Purpose:** Get defenses where professor is assigned as jury member  
**Headers:** `X-Professor-Id: <professor_id>` (temporary, replace with auth)

**Response:**
```json
[
  {
    "id": 13,
    "title": "cpp project",
    "studentName": "Test Student",
    "domain": "Other",
    "status": "scheduled",
    "aiSummary": "...",
    "juryRole": "president"
  }
]
```

**Dependencies:**
- ⚠️ Professor Dashboard main page
- Requires: JuryMember records linking professor to defense

---

### Manager/Defense Endpoints
**Base:** `/api/defenses/`

#### GET /api/defenses/
**Purpose:** Get all thesis defenses (for manager dashboard)  
**Response:** Array of defenses with student, report, jury_members

**Dependencies:**
- ⚠️ Manager Dashboard → Requests page (shows ALL)
- ⚠️ Manager Dashboard → Soutenances page (filters accepted only)
- Frontend: `/dashboard/requests` and `/dashboard/defenses`

#### PATCH /api/defenses/{id}/
**Purpose:** Update defense status, date, time  
**Request:**
```json
{
  "status": "accepted",
  "defense_date": "2025-01-15",
  "defense_time": "14:00"
}
```

**Dependencies:**
- ⚠️ Schedule defense sheet component
- Called when manager schedules a defense

#### POST /api/defenses/{id}/jury/
**Purpose:** Assign professor as jury member  
**Request:**
```json
{
  "thesis_defense_id": 13,
  "professor_id": 5,
  "role": "president"
}
```

**Roles:** "president", "secretary", "examiner", "member"

**Dependencies:**
- ⚠️ CRITICAL: Schedule defense sheet
- ⚠️ Professor dashboard depends on these records

#### GET /api/defenses/{id}/jury-suggestions
**Purpose:** AI-powered jury recommendations  
**Response:**
```json
[
  {
    "professor_id": 5,
    "name": "Ahmed Alami",
    "reason": "Specialty match: Artificial Intelligence & Machine Learning"
  }
]
```

**Dependencies:**
- ✅ AI service (`backend/app/services/jury_ai.py`)
- ✅ Professor specialties must be populated
- ⚠️ Manager dashboard schedule sheet (shows AI suggestions)

---

### Stats Endpoint
**Base:** `/api/stats/`

#### GET /api/stats/
**Purpose:** Dashboard statistics  
**Response:**
```json
{
  "total_thesis_defenses": 1,
  "total_students": 1,
  "total_professors": 3,
  "thesis_defenses_by_status": {
    "pending": 1,
    "accepted": 0,
    "declined": 0
  },
  "monthly_thesis_defenses": [...]
}
```

**Dependencies:**
- ⚠️ Manager Dashboard home page (charts and cards)

---

## 🔐 Authentication Integration Guide for Achraf

### What You Need to Implement

#### 1. Authentication Endpoints
```python
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
GET /api/auth/me
```

#### 2. Replace Mock Authentication

**Current temporary auth (REMOVE THESE):**

**Backend:**
- `X-Professor-Id` header in `/api/professors/` endpoints
- `localStorage.getItem('professorId')` in frontend interceptor

**Frontend:**
```typescript
// frontend/services/api.ts (line 13-18)
api.interceptors.request.use((config) => {
  // TODO: Replace this with real JWT token
  const professorId = localStorage.getItem('professorId') || '1'
  config.headers['X-Professor-Id'] = professorId
  return config
})
```

**Replace with:**
```typescript
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})
```

#### 3. Critical: User Role Detection

The app uses `user.role` to determine which dashboard to show:
- `"student"` → `/student`
- `"professor"` → `/professor/dashboard`
- `"manager"` → `/dashboard`

**Your auth must:**
1. Return `role` field in user object
2. Store it in frontend (localStorage or context)
3. Redirect to correct dashboard after login

#### 4. Protect Routes

**Backend - Add dependency:**
```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(token = Depends(security)):
    # Your JWT decode logic
    return user

# Then use in routes:
@router.get("/assigned-soutenances")
async def get_assigned_soutenances(
    current_user = Depends(get_current_user),  # Replace get_current_professor
    db: Session = Depends(get_db)
):
    professor_id = current_user.id  # Use real user ID
    ...
```

**Frontend - Add route guards:**
```typescript
// Add to each dashboard page
useEffect(() => {
  const token = localStorage.getItem('authToken')
  if (!token) {
    router.push('/login')
  }
}, [])
```

---

## ⚠️ CRITICAL: Database Schema - DO NOT CHANGE

### Tables and Relationships

```
users
├── id (PK)
├── email (UNIQUE)
├── first_name
├── last_name
├── cni (nullable)
├── role (student/professor/manager)
└── (add your auth fields: password_hash, etc.)

students
├── user_id (FK → users.id) ⚠️ DO NOT RENAME
├── major
├── cne
└── year

professors
├── user_id (FK → users.id) ⚠️ DO NOT RENAME
└── specialty ⚠️ CRITICAL: Used by AI

thesis_defenses
├── id (PK)
├── student_id (FK → users.id) ⚠️ DO NOT RENAME
├── title
├── status (pending/accepted/declined)
├── defense_date
├── defense_time
└── report_id (FK → reports.id)

reports
├── id (PK)
├── student_id (FK → users.id)
├── file_name
├── ai_summary ⚠️ Generated by Gemini
├── ai_domain ⚠️ Generated by Gemini
├── ai_similarity_score ⚠️ Generated by Gemini
└── submission_date

jury_members ⚠️ CRITICAL TABLE
├── thesis_defense_id (FK → thesis_defenses.id)
├── professor_id (FK → users.id)
└── role (president/secretary/examiner/member)
```

---

## 🚨 Before You Commit - Checklist

### DO:
- ✅ Add authentication endpoints
- ✅ Add JWT token handling
- ✅ Add password hashing
- ✅ Create login/register pages
- ✅ Add route guards
- ✅ Test with existing endpoints

### DO NOT:
- ❌ Rename `user_id` fields (breaks all relationships)
- ❌ Change `user.role` values (breaks dashboard routing)
- ❌ Remove `professor.specialty` (breaks AI jury suggestions)
- ❌ Change response structure of existing endpoints
- ❌ Remove any fields from User model (add new ones only)
- ❌ Modify AI service imports or calls

---

## 🔧 Testing After Auth Integration

### 1. Test Student Flow
```bash
# Login as student → Should redirect to /student
# Submit request → Should use real user ID from JWT
# View requests → Should show only current student's requests
```

### 2. Test Professor Flow
```bash
# Login as professor → Should redirect to /professor/dashboard
# Check X-Professor-Id header is replaced with JWT
# Assigned soutenances should show based on JWT user ID
```

### 3. Test Manager Flow
```bash
# Login as manager → Should redirect to /dashboard
# Should see all defenses
# AI jury suggestions should still work
```

### 4. Critical: Test Jury Assignment
```bash
# As manager, schedule a defense
# Assign professors to jury
# Verify professor can see it in their dashboard
```

---

## 📞 Contact Points

**AI Features Owner:** Khalid  
**Frontend/UI:** Team  
**Backend API:** Team  
**Authentication:** Achraf (you!)

**If you're unsure about a change, ask in the team chat BEFORE modifying:**
- User model structure
- Foreign key fields
- Existing API endpoints
- Professor specialty field

---

## 🎯 TL;DR - Quick Reference

### Don't Touch These Files (Unless Coordinating):
- ❌ `backend/app/services/ai.py` (AI summary/domain)
- ❌ `backend/app/services/jury_ai.py` (AI jury recommendations)
- ❌ `backend/app/models/*.py` (add auth fields, don't rename existing)
- ❌ `backend/app/api/student.py` (student submission logic)
- ❌ `frontend/services/api.ts` (just update interceptor for JWT)

### Files You'll Mainly Work On:
- ✅ `backend/app/api/auth.py` (new file - your endpoints)
- ✅ `frontend/app/login/page.tsx` (new file - login page)
- ✅ `frontend/app/register/page.tsx` (new file - register page)
- ✅ `frontend/components/AuthGuard.tsx` (new file - route protection)
- ✅ `backend/app/models/user.py` (add password_hash, last_login, etc.)

### Replace This:
```typescript
// frontend/services/api.ts
const professorId = localStorage.getItem('professorId') || '1'
config.headers['X-Professor-Id'] = professorId
```

### With This:
```typescript
const token = localStorage.getItem('authToken')
if (token) config.headers['Authorization'] = `Bearer ${token}`
```

---

**Good luck with the auth implementation! 🚀**  
**Remember: When in doubt, ask the team before changing existing code.**
