# Quick Start Guide - Using AI Features

## For Students

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
