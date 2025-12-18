# 🚀 Setup avec Docker - Checklist Complète

## 📋 Étapes à Suivre (du README)

### ✅ 1. Prérequis Installés
- [x] Python 3.11+
- [x] Node.js 18+
- [ ] **Docker Desktop** ← À installer si pas fait
- [x] Git

**Installer Docker Desktop:**
- Windows/Mac: https://www.docker.com/products/docker-desktop
- Linux: `sudo apt-get install docker.io docker-compose`

---

### ✅ 2. Démarrer PostgreSQL avec Docker

```bash
# À partir de la racine du projet (Ai_Soutenance/)
docker-compose up -d
```

**Vérifier que c'est lancé:**
```bash
docker ps
# Devrait afficher: ai_soutenance_db (Postgres 15)
```

**Configuration:**
- Host: `localhost`
- Port: `5432`
- User: `postgres`
- Password: `12345`
- Database: `ai_Soutenance`

---

### ✅ 3. Setup Backend (FastAPI)

```bash
cd backend

# Créer venv
python -m venv venv

# Activer venv (Windows)
venv\Scripts\activate

# Installer dépendances
pip install -r requirements.txt

# Créer données test (si script existe)
# python scripts/create_test_data.py

# Lancer le serveur
uvicorn app.main:app --reload
```

**Backend:** http://localhost:8000  
**Swagger Docs:** http://localhost:8000/docs

---

### ✅ 4. Setup Frontend (Next.js)

```bash
cd ../frontend

# Installer dépendances
npm install

# Lancer dev server
npm run dev
```

**Frontend:** http://localhost:3000

---

## 🔄 Git - Pull & Merge (Branche dev)

**Si tu veux récupérer les changements du camarade:**

```bash
# 1. Aller à la racine du projet
cd Ai_Soutenance

# 2. Afficher les branches
git branch -a

# 3. Créer/passer à la branche dev
git checkout dev
# ou si elle n'existe pas:
git checkout -b dev origin/dev

# 4. Récupérer les derniers changements
git pull origin dev

# 5. Merger dev dans main (ou ta branche actuelle)
git checkout main
git merge dev

# 6. En cas de conflits, résoudre puis:
git add .
git commit -m "Merge dev branch"
git push origin main
```

---

## 📝 Configuration Requise

### .env Backend (déjà configuré ✅)
```
DATABASE_URL=postgresql://postgres:12345@localhost:5432/ai_Soutenance
API_HOST=0.0.0.0
API_PORT=8000
```

### .env Frontend (déjà configuré ✅)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🧪 Test Rapide

```bash
# Test PostgreSQL
docker exec ai_soutenance_db psql -U postgres -d ai_Soutenance -c "SELECT 1"

# Test Backend API
curl -H "X-Professor-Id: 1" http://localhost:8000/api/professors/assigned-soutenances

# Test Frontend
# Ouvrir http://localhost:3000 dans le navigateur
```

---

## 🐳 Commandes Docker Utiles

```bash
# Démarrer la base de données
docker-compose up -d

# Arrêter
docker-compose down

# Voir les logs
docker-compose logs -f

# Accéder à la DB en ligne de commande
docker exec -it ai_soutenance_db psql -U postgres -d ai_Soutenance

# Réinitialiser la DB (⚠️ supprime tout)
docker-compose down -v
docker-compose up -d
```

---

## 🎯 Étapes à Suivre (Résumé)

1. **Installer Docker Desktop** (si pas fait)
2. **Démarrer PostgreSQL:** `docker-compose up -d`
3. **Vérifier la connexion:** `docker ps`
4. **Setup Backend:**
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
5. **Setup Frontend:**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```
6. **Tester:** http://localhost:3000

---

## 📊 Architecture Finale

```
Docker PostgreSQL (localhost:5432)
    ↓
FastAPI Backend (http://localhost:8000)
    ↓
Next.js Frontend (http://localhost:3000)
```

---

## ✨ Points Importants du README

✅ **Database:** PostgreSQL avec Docker (pas SQLite)  
✅ **Backend:** FastAPI sur port 8000  
✅ **Frontend:** Next.js sur port 3000  
✅ **API Docs:** http://localhost:8000/docs (Swagger)  
✅ **Roles:** Student, Professor, Manager  
✅ **Features:** AI analysis, PDF upload, jury assignment  

---

## 🔄 Merger avec ton travail

**Ton travail actuellement:**
- ✅ 6 endpoints implémentés (professors)
- ✅ Frontend connecté au backend
- ✅ CORS configuré
- ✅ Données seedées (SQLite)

**À faire après merge de dev:**
1. Adapter le seed pour PostgreSQL (au lieu de SQLite)
2. Vérifier les endpoints student/thesis_defense si présents dans dev
3. Tester la chaîne complète Docker → Backend → Frontend

---

**Prêt? Commencez par:** `docker-compose up -d` 🚀
