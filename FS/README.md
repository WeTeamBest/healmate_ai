# 🏥 HealMate AI - Platform Konseling Emosi Berbasis AI

Aplikasi web untuk membantu orang yang sedang pulih dari putus cinta. Lengkap dengan fitur chat dengan AI konselor, tracking mood harian, setting goals pemulihan, dan time capsule (tulis pesan untuk diri sendiri di masa depan).

---

## 🎯 Apa Itu HealMate?

HealMate adalah aplikasi web yang nemenin perjalanan pemulihan emosional kamu. Dengan bantuan AI, aplikasi ini bisa:

- 💬 **Dengarkan & Bantu** - Chat dengan AI Partner yang empatik
- 😊 **Pantau Mood** - Track mood harian dan lihat progressmu
- 🎯 **Atur Goals** - Set target pemulihan dan track pencapaiannya
- 📮 **Kirim Pesan** - Tulis pesan untuk diri sendiri di masa depan

---

## ⚡ Mulai Dalam 5 Menit

### Opsi 1: Pakai Docker (Paling Gampang)

```bash
# 1. Masuk ke folder project
cd FS

# 2. Copy file konfigurasi
cp .env.example .env

# 3. Edit .env - isi 2 hal:
#    - MONGODB_URI (tempat nyimpen data)
#    - GEMINI_API_KEY (API key untuk AI)

# 4. Jalankan semua service
docker-compose up -d

# ✅ Done! Buka di browser:
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Opsi 2: Setup Manual

**A. Backend (Python + FastAPI)**

```bash
cd backend-fastapi-full

# Buat isolated Python environment
python -m venv venv

# Aktifkan (Linux/Mac):
source venv/bin/activate
# Atau untuk Windows:
# venv\Scripts\activate

# Install library
pip install -r requirements.txt

# Copy & edit file config
cp .env.example .env
# Edit .env - sesuaikan MONGODB_URI & GEMINI_API_KEY

# Jalankan backend
uvicorn main:app --reload
```

Backend akan jalan di `http://localhost:8000`

**B. Frontend (React + JavaScript)**

```bash
cd frontend

# Install library
npm install

# Jalankan dev server
npm run dev
```

Frontend akan jalan di `http://localhost:5173`

**C. Database (MongoDB)**

Pilih salah satu:

**Opsi A: Local MongoDB (Paling simple)**
```bash
# Install MongoDB dari: https://docs.mongodb.com/manual/installation/
# Jalankan:
mongod
```

**Opsi B: Cloud MongoDB (Recommended untuk production)**
1. Buat akun gratis di https://www.mongodb.com/cloud/atlas
2. Buat cluster baru
3. Copy connection string
4. Paste ke `MONGODB_URI` di file `.env`

---

## 🔧 Konfigurasi (.env) - Data Penting

Buat file `.env` di folder `backend-fastapi-full/`. File ini nyimpen konfigurasi sensitif (jangan di-commit ke git!).

```env
# ════════════════════════════════════════════════════════════
# 🗄️ DATABASE - Tempat nyimpen semua data
# ════════════════════════════════════════════════════════════

# Opsi 1: Local MongoDB (untuk development)
MONGODB_URI=mongodb://localhost:27017/healmate

# Opsi 2: MongoDB Atlas Cloud (untuk production)
# MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/healmate?retryWrites=true&w=majority

# Opsi 3: Docker MongoDB
# MONGODB_URI=mongodb://mongodb:27017/healmate
# MONGO_USER=admin
# MONGO_PASSWORD=your_password_here


# ════════════════════════════════════════════════════════════
# 🤖 GEMINI API - Untuk AI Konselor
# ════════════════════════════════════════════════════════════

# Dapatkan API key di: https://ai.google.dev
# 1. Buka link di atas
# 2. Click "Get API Key"
# 3. Copy-paste di sini
GEMINI_API_KEY=your_gemini_api_key_here


# ════════════════════════════════════════════════════════════
# 🔐 JWT - Untuk Secure Login
# ════════════════════════════════════════════════════════════

# Secret key (GANTI INI DI PRODUCTION!)
# Generate random: python -c "import secrets; print(secrets.token_urlsafe(32))"
JWT_SECRET=dev-secret-key-change-this-in-production

JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


# ════════════════════════════════════════════════════════════
# 🌍 ENVIRONMENT
# ════════════════════════════════════════════════════════════

# Pilih: development, staging, atau production
ENVIRONMENT=development


# ════════════════════════════════════════════════════════════
# 🌐 CORS - Domain Frontend yang Diizinkan
# ════════════════════════════════════════════════════════════

# Development:
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Production (update dengan domain kamu):
# ALLOWED_ORIGINS=https://healmate.example.com


# ════════════════════════════════════════════════════════════
# 📡 SERVER SETTINGS
# ════════════════════════════════════════════════════════════

HOST=0.0.0.0
PORT=8000
DEBUG=true
LOG_LEVEL=INFO
```

---

## 📱 Fitur Utama

### 1. Chat dengan AI Konselor 💬
Ketik keluh kesahmu, dan AI akan balik dengan jawaban yang empatik dan supportif. Dilengkapi dengan emotion detection otomatis yang mengenali emosi kamu (anxiety, anger, acceptance) dan memberikan saran aktivitas healing yang personal.

### 2. Mood Tracking 📊
Log mood kamu setiap hari dengan scale 1-10. Lihat grafik tren mood dari waktu ke waktu, dan tulis catatan pribadi untuk setiap log yang kamu buat.

### 3. Goal Setting 🎯
Buat healing goals untuk perjalanan pemulihan kamu. Track progress, get reminder, dan celebrate setiap milestone yang tercapai.

### 4. Time Capsule 📮
Tulis pesan untuk diri sendiri. Set kapan pesan itu dibuka (bisa minggu depan, sebulan depan, setahun depan). Baca pesan kamu di waktu yang sudah ditentukan.

### 5. Dashboard 📈
Lihat overview mood stats kamu, progress tracking, dan recent chats semuanya dalam satu dashboard yang user-friendly.

---

## 🧪 Test Aplikasi

### 1. Cek Backend Hidup

```bash
curl http://localhost:8000/api/health
```

Harusnya dapat response:
```json
{"status": "success", "timestamp": "2026-06-02T10:00:00Z"}
```

### 2. Test Register & Login

**Register user baru:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Kalo dapat token, artinya login berhasil!

### 3. Coba Aplikasi di Browser

Buka http://localhost:5173

- Register akun baru
- Login
- Chat sama AI konselor
- Cek emotion detection & healing score
- Try semua fitur lainnya

---

## 📁 Struktur Project

Sebelum mulai coding, bagus tahu dimana file-file penting:

```
FS/
├── frontend/                    ← React App
│   ├── src/
│   │   ├── components/          ← UI components (Button, Card, dll)
│   │   ├── pages/               ← Pages (ChatPage, DashboardPage, dll)
│   │   ├── services/            ← API call utilities
│   │   ├── stores/              ← State management (Zustand)
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
│
├── backend-fastapi-full/        ← Python Backend
│   ├── main.py                  ← App entry point
│   ├── config.py                ← Configuration loader
│   ├── requirements.txt          ← Python dependencies
│   ├── ai/                       ← Emotion detection models
│   ├── routes/                   ← API endpoints
│   │   ├── auth.py              ← Login/Register
│   │   ├── chat.py              ← Chat endpoints
│   │   ├── mood.py              ← Mood tracking
│   │   ├── goals.py             ← Goal management
│   │   └── timecapsule.py       ← Time capsule
│   ├── services/                ← Business logic
│   ├── middleware/              ← Auth middleware
│   ├── models/                  ← Database models
│   ├── utils/                   ← Helper functions
│   ├── .env.example
│   └── Dockerfile
│
└── docker-compose.yml           ← Container orchestration
```

---

## 🐛 Troubleshooting - Kalo Ada Masalah

### ❌ Port 8000 atau 5173 Sudah Dipakai

```bash
# Cari process yang pakai port
lsof -i :8000
lsof -i :5173

# Kill process (ganti XXX dengan PID number)
kill -9 XXX
```

### ❌ MongoDB Ga Connect

**Error:** `Error: connect ECONNREFUSED 127.0.0.1:27017`

**Fix:**
- Pastikan MongoDB running dengan command: `mongod` (di terminal lain)
- Atau gunakan MongoDB Atlas cloud
- Pastikan `MONGODB_URI` di `.env` benar

### ❌ Gemini API Key Invalid

**Error:** `API key invalid or expired`

**Fix:**
- Regenerate key di https://ai.google.dev
- Update di `.env`
- Restart backend dengan `uvicorn main:app --reload`

### ❌ Frontend Ga Bisa Connect Backend

**Error:** `Failed to fetch from http://localhost:8000`

**Fix:**
- Pastikan backend running: buka http://localhost:8000/api/health
- Check `VITE_API_URL` value di frontend
- Restart frontend

### ❌ Token JWT Error

**Error:** `Invalid token or expired`

**Fix:**
- Login lagi untuk dapat token baru
- Pastikan `JWT_SECRET` di `.env` sama antara restart
- Check `ACCESS_TOKEN_EXPIRE_MINUTES` value

---

## 🔗 Link Penting

- **Frontend Code**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **MongoDB Local Shell**: `mongosh`
- **Gemini API Setup**: https://ai.google.dev
- **MongoDB Cloud**: https://www.mongodb.com/cloud/atlas

---

## 🚀 Deploy ke Production

Sebelum deploy ke production server, jangan lupa:

- ✅ **Ubah JWT_SECRET** ke random string yang aman
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- ✅ **Ubah ENVIRONMENT** ke `production`
- ✅ **Ubah DEBUG** ke `false`
- ✅ **Gunakan MongoDB Atlas** (jangan local)
- ✅ **Setup HTTPS** (gunakan SSL certificate)
- ✅ **Update ALLOWED_ORIGINS** dengan domain production kamu
- ✅ **Configure logging & monitoring**
- ✅ **Setup database backup**

---

## 💡 Tips Development

### Hot Reload
- **Backend**: FastAPI dengan `--reload` flag otomatis reload pas ada code changes
- **Frontend**: Vite udah support HMR (Hot Module Replacement) secara otomatis

### Debug Backend
- Buka http://localhost:8000/docs untuk Swagger UI
- Check terminal logs untuk error messages
- Gunakan print statements atau debugger

### Debug Frontend
- Buka browser DevTools (F12)
- Check Console untuk JavaScript errors
- Gunakan Network tab untuk lihat API requests

### Database Inspection
```bash
# Connect ke local MongoDB
mongosh

# Pilih database
use healmate

# Lihat semua collections
show collections

# Query users
db.users.find()

# Query recent chats
db.chats.find().limit(5)
```

---

## 📞 Support & Resources

Butuh bantuan lebih lanjut?

- 📖 **API Documentation**: http://localhost:8000/docs (sudah interactive)
- 🚀 **FastAPI Docs**: https://fastapi.tiangolo.com
- ⚛️ **React Docs**: https://react.dev
- 📊 **MongoDB Manual**: https://docs.mongodb.com/manual
- 🎨 **Vite Guide**: https://vitejs.dev/guide
- 🤖 **Gemini API**: https://ai.google.dev

---

Good luck! Semoga project kamu lancar 🚀
