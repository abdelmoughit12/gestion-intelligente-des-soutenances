# Complete Testing Guide - Authentication & AI Features

## 🚀 Prerequisites

1. **Docker Desktop** must be running
2. **Backend** must be running at http://localhost:8000
3. **Frontend** must be running at http://localhost:3000
4. **PostgreSQL** database must be accessible

---

## 📦 Step 1: Start the Application

### Option A: Using Docker (Recommended)
```bash
# From project root
docker compose down  # Stop any running containers
docker compose up -d --build  # Build and start all services
```

### Option B: Manual Start
```bash
# Terminal 1: Start Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend
cd frontend
npm install
npm run dev
```

### Check Services are Running
```bash
# Check Docker containers
docker compose ps

# Expected output:
# - postgres (running)
# - backend (running on port 8000)
# - frontend (running on port 3000)
```

---

## 👥 Step 2: Create Test Users

The system requires authenticated users for all dashboards. Let's create test users for each role.

### Create Initial Users Script
```bash
# Run the seed script (creates users if not exists)
docker compose exec backend python scripts/create_initial_data.py

# OR manually via Python:
docker compose exec backend python -c "
from app.db.session import SessionLocal
from app.crud import crud_user
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

db = SessionLocal()

# Create manager
manager_data = UserCreate(
    email='manager@example.com',
    password='manager123',
    first_name='Admin',
    last_name='Manager',
    role='manager'
)
crud_user.create(db, obj_in=manager_data)

# Create professor
prof_data = UserCreate(
    email='professor@example.com',
    password='prof123',
    first_name='Ahmed',
    last_name='Alami',
    role='professor'
)
crud_user.create(db, obj_in=prof_data)

# Create student
student_data = UserCreate(
    email='student@example.com',
    password='student123',
    first_name='Ali',
    last_name='Benali',
    role='student'
)
crud_user.create(db, obj_in=student_data)

db.close()
print('Users created successfully!')
"
```

### Test Users Created:
| Role | Email | Password | Access |
|------|-------|----------|--------|
| **Manager** | manager@example.com | manager123 | Full access to all defenses |
| **Professor** | professor@example.com | prof123 | Assigned defenses only |
| **Student** | student@example.com | student123 | Own requests only |

---

## 🧪 Step 3: Test Authentication Flow

### Test 1: Login Page
1. Visit http://localhost:3000
2. **Expected:** Redirected to http://localhost:3000/login
3. **UI Should Show:**
   - Email input field
   - Password input field
   - "Sign In" button

### Test 2: Login as Student
```
✅ Email: student@example.com
✅ Password: student123
✅ Click "Sign In"
✅ Expected: Redirect to /student (Student Dashboard)
```

**Verify:**
- ✅ Student Dashboard loads
- ✅ Sidebar shows "Student Portal"
- ✅ Navigation: Dashboard, New Request, My Requests
- ✅ JWT token stored in localStorage

### Test 3: Login as Professor
```
✅ Email: professor@example.com
✅ Password: prof123
✅ Click "Sign In"
✅ Expected: Redirect to /professor/dashboard
```

**Verify:**
- ✅ Professor Dashboard loads
- ✅ Sidebar shows "Professor Space"
- ✅ Can see assigned defenses (empty initially)

### Test 4: Login as Manager
```
✅ Email: manager@example.com
✅ Password: manager123
✅ Click "Sign In"
✅ Expected: Redirect to /dashboard
```

**Verify:**
- ✅ Manager Dashboard loads
- ✅ Sidebar shows "Manager Dashboard"
- ✅ Can see statistics and all defenses

---

## 📝 Step 4: Test Student Flow (AI Features)

### Test Student Submission with AI Processing

**Login as Student** (student@example.com / student123)

#### 4.1 Create New Thesis Request
1. Click **"New Request"** in sidebar
2. Fill the form:
   - **Title:** "AI-Powered Recommendation System"
   - **Domain:** "Artificial Intelligence"
   - **Upload PDF:** Select any PDF file (test document)
3. Click **"Submit Request"**

**Expected AI Processing:**
- 🤖 Backend extracts PDF text
- 🤖 Gemini generates summary (2-3 sentences)
- 🤖 Gemini classifies domain (AI, Web, IoT, etc.)
- 🤖 Gemini calculates similarity score (0-100)

**Verify:**
4. Check **"My Requests"** page
5. **Should see:**
   - Title: "AI-Powered Recommendation System"
   - Domain: Auto-detected by AI
   - Status: "pending"
   - Summary: AI-generated summary
   - PDF download link

#### 4.2 Check Backend Logs for AI Activity
```bash
docker compose logs backend --tail=50
```

**Look for:**
```
✅ GEMINI SUCCESS - Summary generated: ...
✅ GEMINI SUCCESS - Domain classified: {"AI": 0.85, ...}
✅ GEMINI SUCCESS - Similarity score calculated: 0.75
```

OR if quota exceeded:
```
⚠️ GEMINI FALLBACK - Using fallback model
❌ GEMINI FAILED - Using default values (still works!)
```

#### 4.3 Test Multiple Submissions
Create 2 more requests with different domains:
- **"E-Commerce Web Platform"** → Should detect "Web Development"
- **"Smart IoT Home Automation"** → Should detect "IoT"

**All should appear in "My Requests"**

---

## 🎓 Step 5: Test Manager Flow (AI Jury Recommendations)

### Test Manager Defense Scheduling with AI

**Login as Manager** (manager@example.com / manager123)

#### 5.1 View Pending Requests
1. Click **"Requests"** in sidebar
2. **Should see:** All student submissions (3 requests)
3. **Table columns:**
   - ID
   - Student Name
   - Title
   - Status (all "pending")
   - Actions (three dots menu)

#### 5.2 Schedule Defense with AI Jury Suggestions
1. Click **three dots (⋮)** on first defense
2. Click **"Schedule"**
3. **AI Suggestions appear automatically:**

**Expected UI:**
```
🤖 AI Jury Suggestions
┌────────────────────────────────────────┐
│ Ahmed Alami                      [Add] │
│ Specialty match: AI & Machine Learning │
├────────────────────────────────────────┤
│ Fatima Bennani                   [Add] │
│ Specialty match: Web Development       │
├────────────────────────────────────────┤
│ Mohamed El Idrissi               [Add] │
│ Specialty match: IoT & Embedded Systems│
└────────────────────────────────────────┘
```

4. **Click "Add"** on Ahmed Alami (AI professor)
5. Select **defense date** (e.g., 2025-01-15)
6. Set **defense time** (e.g., 14:00)
7. Assign **roles:**
   - Ahmed Alami → President
8. Click **"Schedule Defense"**

**Verify:**
- ✅ Success toast appears
- ✅ Defense status changes from "pending" to "accepted"
- ✅ Jury member assigned

#### 5.3 Check AI Recommendations API
```bash
# Test AI endpoint directly
curl http://localhost:8000/api/v1/thesis-defenses/1/jury-suggestions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected Response:**
```json
[
  {
    "professor_id": 1,
    "name": "Ahmed Alami",
    "reason": "Specialty match: Artificial Intelligence & Machine Learning"
  },
  ...
]
```

#### 5.4 View Scheduled Defenses
1. Click **"Soutenances"** in sidebar
2. **Should see:** Only accepted/scheduled defenses
3. **Table shows:**
   - Defense date & time
   - Assigned jury members
   - Student name

---

## 👨‍🏫 Step 6: Test Professor Flow

### Test Professor Assigned Defenses

**Login as Professor** (professor@example.com / prof123)

#### 6.1 View Assigned Defenses
1. **Dashboard loads automatically**
2. **Should see:**
   - Assigned defense: "AI-Powered Recommendation System"
   - Role: "President"
   - Status: "Scheduled"
   - **AI Summary:** Shows Gemini-generated summary
   - Defense date & time

#### 6.2 View Defense Details
1. Click on the defense card
2. **Should see:**
   - Full thesis title
   - Student name
   - AI-generated summary (helps professor prepare)
   - AI domain classification
   - PDF download button

#### 6.3 Download Thesis Report
1. Click **"Download Report"** button
2. PDF should download successfully

---

## 🧪 Step 7: Test Authorization & Security

### Test 7.1: Role-Based Access Control

**As Student** (student@example.com):
```
❌ Try to access /dashboard (manager page)
✅ Expected: Redirect to /unauthorized
✅ Message: "You don't have permission to access this page"
```

**As Professor** (professor@example.com):
```
❌ Try to access /dashboard (manager page)
✅ Expected: Redirect to /unauthorized
```

**As Manager** (manager@example.com):
```
❌ Try to access /student
✅ Expected: Redirect to /unauthorized
```

### Test 7.2: JWT Token Expiry
```
1. Login as any user
2. Open Browser DevTools → Application → Local Storage
3. Find "authToken"
4. Wait 30 minutes (ACCESS_TOKEN_EXPIRE_MINUTES)
5. Try to make an API call
✅ Expected: 401 Unauthorized
✅ Expected: Redirect to /login
```

### Test 7.3: API Endpoint Protection
```bash
# Try to access protected endpoint without token
curl http://localhost:8000/api/v1/thesis-defenses/

# Expected: 401 Unauthorized

# Try with valid token
curl http://localhost:8000/api/v1/thesis-defenses/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Expected: 200 OK with data
```

---

## 🔍 Step 8: Test Complete Data Flow

### End-to-End Scenario

**Goal:** Test student submission → AI processing → manager scheduling → professor assignment

#### Complete Flow:
1. **Student** creates request → ✅ AI processes PDF
2. **Manager** views request → ✅ AI suggests jury
3. **Manager** schedules defense → ✅ Jury assigned
4. **Professor** sees assignment → ✅ AI summary helps prepare
5. **Professor** downloads report → ✅ PDF accessible

**Verify Data Consistency:**
```bash
# Check database records
docker compose exec postgres psql -U postgres -d Ai_Soutenance

# Run SQL:
SELECT td.id, td.title, td.status, r.ai_summary IS NOT NULL as has_ai, 
       COUNT(jm.id) as jury_count
FROM thesis_defenses td
LEFT JOIN reports r ON r.student_id = td.student_id
LEFT JOIN jury_members jm ON jm.thesis_defense_id = td.id
GROUP BY td.id, td.title, td.status, r.ai_summary;

# Expected output shows all defenses with AI data and jury counts
```

---

## 🐛 Step 9: Troubleshooting

### Issue: "Backend server is not running"
```bash
# Check backend status
docker compose ps backend

# Check backend logs
docker compose logs backend --tail=50

# Restart if needed
docker compose restart backend
```

### Issue: "Failed to fetch defenses"
```bash
# Check if JWT token exists
# Browser DevTools → Application → Local Storage → authToken

# If missing, login again
# If exists, check backend logs for 401 errors
```

### Issue: "AI features not working"
```bash
# Check Gemini API key
cat backend/.env | grep GEMINI_API_KEY

# Check backend logs for AI errors
docker compose logs backend | grep GEMINI

# Common: Quota exceeded (system uses fallback, still works)
```

### Issue: "No jury suggestions"
```bash
# Check if professors have specialties
docker compose exec postgres psql -U postgres -d Ai_Soutenance \
  -c "SELECT id, specialty FROM professors;"

# Add professors if missing:
docker compose exec backend python -c "
from app.db.session import SessionLocal
from app import models

db = SessionLocal()
# Run seed script from backend/seed_professors.sql
"
```

---

## ✅ Step 10: Verification Checklist

### Authentication ✅
- [ ] Login page loads
- [ ] Login with student credentials works
- [ ] Login with professor credentials works
- [ ] Login with manager credentials works
- [ ] JWT token stored in localStorage
- [ ] Logout clears token
- [ ] Unauthorized access blocked

### Student Features ✅
- [ ] Can submit thesis request
- [ ] PDF upload works
- [ ] AI summary generated
- [ ] AI domain classified
- [ ] Similarity score calculated
- [ ] Can view own requests only
- [ ] Cannot access manager/professor pages

### Manager Features ✅
- [ ] Can view all defenses
- [ ] Statistics dashboard works
- [ ] AI jury suggestions appear
- [ ] Can schedule defenses
- [ ] Can assign jury members
- [ ] Can view reports

### Professor Features ✅
- [ ] Can view assigned defenses only
- [ ] AI summary visible
- [ ] Can download reports
- [ ] Cannot access student/manager pages

### AI Features ✅
- [ ] PDF text extraction works
- [ ] Gemini summary generation works
- [ ] Domain classification works
- [ ] Jury recommendations work
- [ ] Fallback logic works on rate limit
- [ ] Logs show AI activity

---

## 📊 Expected Test Results

### Database State After Complete Testing:
```
- 3 users (student, professor, manager)
- 3 thesis defenses (all with AI data)
- 3 reports (all with AI summaries)
- 1+ jury members assigned
- All auth tokens valid
```

### API Endpoints Working:
```
✅ POST /api/v1/auth/login
✅ GET  /api/v1/students/soutenance-requests
✅ POST /api/v1/students/soutenance-requests
✅ GET  /api/v1/thesis-defenses/
✅ GET  /api/v1/thesis-defenses/{id}/jury-suggestions
✅ POST /api/v1/thesis-defenses/{id}/jury/
✅ GET  /api/v1/professors/assigned-soutenances
✅ GET  /api/v1/stats/
```

### Frontend Routes Working:
```
✅ /login (public)
✅ /student (student only)
✅ /professor/dashboard (professor only)
✅ /dashboard (manager only)
✅ /unauthorized (all)
```

---

## 🎯 Summary

**What We Tested:**
1. ✅ Authentication system (JWT, login, roles)
2. ✅ Student thesis submission with AI processing
3. ✅ Manager jury scheduling with AI recommendations
4. ✅ Professor dashboard with assigned defenses
5. ✅ Role-based access control
6. ✅ Complete data flow
7. ✅ API security
8. ✅ AI features (summary, domain, jury suggestions)

**Key Features Verified:**
- 🔐 Secure authentication with JWT
- 🤖 AI-powered PDF analysis (Gemini)
- 🤖 Smart jury recommendations
- 👥 Role-based dashboards
- 🔒 Protected API endpoints
- ✨ Modern UI with React/Next.js

**All systems working!** 🎉

---

## 📞 Support

**Issues? Check:**
1. Docker containers running: `docker compose ps`
2. Backend logs: `docker compose logs backend --tail=50`
3. Frontend logs: `docker compose logs frontend --tail=50`
4. Database connection: `docker compose exec postgres psql -U postgres -d Ai_Soutenance`

**Documentation:**
- [API_ENDPOINTS_AND_DEPENDENCIES.md](./API_ENDPOINTS_AND_DEPENDENCIES.md) - API reference
- [AI_FEATURES_SUMMARY.md](./AI_FEATURES_SUMMARY.md) - AI features documentation
- [MERGE_CONFLICT_ANALYSIS.md](./MERGE_CONFLICT_ANALYSIS.md) - Recent changes

**Team Members:**
- Authentication: Achraf
- AI Features: Khalid
- Frontend/UI: Team
- Backend API: Team

### Submitting a Thesis Defense Request

1. Navigate to **Student Dashboard** → **New Request**
2. Fill in the form:
   - Title: Your thesis title
   - Domain: Your research domain
   - Upload PDF: Your thesis report
3. Click **Submit Request**

**What Happens Behind the Scenes:**
- 🤖 AI reads your PDF and generates a summary
- 🤖 AI classifies your thesis domain
- 🤖 AI calculates a similarity score between title and content
- ✅ Your request is saved with AI-generated metadata

**Where to See AI Results:**
- View your request in the **Request History** table
- Summary and domain are stored in the database
- Manager can see this AI data when reviewing your request

---

## For Managers

### Scheduling a Defense with AI Jury Suggestions

1. Navigate to **Manager Dashboard** → **Defenses**
2. Click the **Schedule** button on any pending defense
3. Fill in date and time

**AI Jury Suggestions Appear Automatically:**
- 🤖 Blue card shows "AI Jury Suggestions"
- Top 3 recommended professors based on thesis domain
- Each suggestion includes reasoning (e.g., "Specialty match: Artificial Intelligence")
- Click **Add** button to quickly select suggested professors

4. Assign roles to jury members (president, secretary, examiner, member)
5. Click **Schedule Defense**

**Benefits:**
- ✅ No manual searching through professor list
- ✅ AI matches thesis domain with professor specialties
- ✅ Faster scheduling with smart recommendations
- ✅ Still can manually add other professors if needed

---

## For Professors

### Viewing Assigned Defenses

1. Navigate to **Professor Dashboard**
2. View your assigned soutenances
3. See AI-generated summaries of student theses

**Coming Soon:**
- 🔜 AI-generated evaluation hints
- 🔜 Key points extraction from reports
- 🔜 Suggested evaluation criteria

---

## Testing the Features

### Test AI Jury Suggestions (API)
```bash
# Replace 13 with your defense ID
curl http://localhost:8000/api/defenses/13/jury-suggestions
```

Expected response:
```json
[
  {
    "professor_id": 5,
    "name": "Ahmed Alami",
    "reason": "Specialty match: Artificial Intelligence & Machine Learning"
  },
  ...
]
```

### Test Student Submission (Frontend)
1. Go to http://localhost:3000/dashboard/requests
2. Click "New Request"
3. Fill form and upload a PDF
4. Check the database:
```sql
SELECT id, title, ai_summary, ai_domain FROM thesis_defenses;
```

### Monitor AI Activity (Logs)
```bash
# Watch backend logs in real-time
docker compose logs -f backend

# Look for:
# ✅ GEMINI SUCCESS - Feature working perfectly
# ⚠️ GEMINI FALLBACK - Using backup model (still works)
# ❌ GEMINI FAILED - Using fallback logic (still works)
```

---

## Troubleshooting

### AI Suggestions Not Showing
1. Check if defense has a domain: `SELECT ai_domain FROM thesis_defenses WHERE id = 13;`
2. Check if professors have specialties: `SELECT id, specialty FROM professors;`
3. Check backend logs: `docker compose logs backend --tail=50`

### Gemini API Errors
- **429 Quota Exceeded**: System automatically uses fallback logic, still works
- **401 Unauthorized**: Check GEMINI_API_KEY in `backend/.env`
- **Connection Error**: AI gracefully degrades, system continues working

### No Professors in Suggestions
1. Make sure professors have specialties set
2. Run seed script: `Get-Content .\backend\seed_professors.sql | docker compose exec -T postgres psql -U postgres -d Ai_Soutenance`

---

## Tips & Best Practices

### For Better AI Results

**Students:**
- Use descriptive thesis titles
- Ensure PDF has clear text (not scanned images)
- Domain field helps AI classify better

**Managers:**
- Review AI suggestions but trust your judgment
- AI is a helper, not a decision maker
- You can always manually add other professors

**Admins:**
- Keep professor specialties up to date
- Monitor AI usage with logs
- Consider upgrading Gemini plan for production

---

## Visual Guide

### Student Dashboard - New Request Form
```
┌─────────────────────────────────────┐
│ 📝 New Soutenance Request           │
├─────────────────────────────────────┤
│ Title: [________________]           │
│ Domain: [________________]          │
│ Upload PDF: [Choose File]           │
│                                     │
│          [Submit Request]           │
└─────────────────────────────────────┘
         ↓ (AI Processing)
    🤖 Summary generated
    🤖 Domain classified
    🤖 Similarity scored
```

### Manager Dashboard - Schedule Defense
```
┌─────────────────────────────────────┐
│ 📅 Schedule Defense                 │
├─────────────────────────────────────┤
│ Date: [2024-01-15]                  │
│ Time: [14:00]                       │
│                                     │
│ ┌─ 🤖 AI Jury Suggestions ────────┐│
│ │ Ahmed Alami                      ││
│ │ Specialty match: AI & ML    [Add]││
│ │                                  ││
│ │ Fatima Bennani                   ││
│ │ Specialty match: Web Dev    [Add]││
│ └──────────────────────────────────┘│
│                                     │
│ Jury Members: [Select Professors]   │
│                                     │
│      [Schedule Defense]             │
└─────────────────────────────────────┘
```

---

## Next Steps

1. ✅ Test student submission with real PDF
2. ✅ Test manager scheduling with AI suggestions
3. 🔜 Add more professors with specialties
4. 🔜 Implement professor evaluation assistance
5. 🔜 Add report quality analysis

---

## Support

For issues or questions:
1. Check logs: `docker compose logs backend`
2. Review API docs: http://localhost:8000/docs
3. Check database: Connect to PostgreSQL
4. Review this guide and AI_FEATURES_SUMMARY.md
