# 🏥 HealMate AI – Powered Emotional Recovery Platform

## 📋 Project Overview

HealMate AI merupakan platform pemulihan emosional berbasis kecerdasan buatan dengan mengintegrasikan LLM yang dirancang untuk membantu individu menghadapi fase pasca putus cinta melalui dukungan digital yang empatik, personal, dan berbasis data. Sistem ini mengintegrasikan teknologi LLM, Data Science, dan Web Development untuk menyediakan pengalaman pendampingan emosional yang lebih interaktif dan terukur.

Proyek ini dikembangkan melalui kolaborasi tiga domain utama:

### 💻 Full Stack Development

Tim Full Stack bertanggung jawab membangun aplikasi web HealMate AI menggunakan React, FastAPI, dan MongoDB. Platform menyediakan berbagai fitur seperti AI Chat Counseling, Mood Tracking, Goal Management, Dashboard Monitoring, dan Time Capsule yang dirancang untuk mendukung perjalanan pemulihan emosional pengguna.

### 📊 Data Science

Tim Data Science mengembangkan pipeline pengolahan data mulai dari pengumpulan dataset, data cleaning, emotion labeling, exploratory data analysis (EDA), hingga perancangan metrik **Healing Score**. Dataset yang dihasilkan berfokus pada konteks pemulihan pasca putus cinta dan menjadi fondasi utama dalam pengembangan model AI.

### 🤖 Artificial Intelligence

Tim AI membangun sistem deteksi emosi berbasis Deep Learning yang mampu mengidentifikasi emosi pengguna ke dalam kategori **Anxiety**, **Anger**, dan **Acceptance**. Selain melakukan klasifikasi emosi, model juga memprediksi **Healing Score** untuk mengukur tingkat pemulihan emosional pengguna. Hasil prediksi kemudian diintegrasikan dengan Gemini AI untuk menghasilkan respons konseling dan rekomendasi aktivitas yang lebih personal.

---

## 🎯 Project Objectives

* Membantu pengguna memahami dan mengelola kondisi emosional mereka.
* Menyediakan pendamping emosional berbasis LLM yang dapat diakses kapan saja.
* Melakukan deteksi dan analisis emosi secara otomatis.
* Mengukur tingkat pemulihan emosional melalui Healing Score.
* Memberikan rekomendasi dan dukungan yang dipersonalisasi berdasarkan kondisi pengguna.
* Mengintegrasikan teknologi LLM, Data Science, dan Web Development dalam satu ekosistem aplikasi yang terintegrasi.

---

## ✨ Key Features

* 💬 AI Emotional Counseling Chat
* 😊 Mood Tracking & Emotional Monitoring
* 🎯 Goal Setting & Progress Tracking
* 📮 Time Capsule for Self Reflection
* 🧠 Emotion Detection (Anxiety, Anger, Acceptance)
* 📊 Healing Score Prediction
* 🤖 Gemini AI Integration
* 📈 Personal Recovery Dashboard
* 🔒 Secure Authentication & User Management

---

## 🏗️ Project Structure

```text
HealMate-AI/
│
├── AI/                         # LLM Integration
│   ├── dataset/
│   ├── Main/
│   ├── inference/
│   ├── REST API/
│   └── README.md
│
├── DS/                         # Data Science Pipeline
│   ├── Dashboard Streamlit/
│   ├── Emotion Label/
│   ├── Empathetic Counseling Dataset/
│   └── README.md
│
├── FS/                         # Full Stack Application
│   ├── frontend/
│   ├── backend-fastapi-full/
│   ├── docker-compose.yml
│   └── README.md
│
└── README.md                   # Main Project Documentation
```

---

## 📚 Learning Path Documentation

Setiap learning path memiliki dokumentasi teknis yang lebih lengkap:

### 🤖 Artificial Intelligence

https://github.com/WeTeamBest/healmate_ai/blob/main/AI/README.md

### 📊 Data Science

https://github.com/WeTeamBest/healmate_ai/blob/main/DS/README.md

### 💻 Full Stack Development

https://github.com/WeTeamBest/healmate_ai/blob/main/FS/README.md

---

## 🧠 Pretrained Models & Training Results

Seluruh hasil pelatihan model, artefak pendukung, dan file deployment dapat diakses melalui Google Drive berikut:

**Google Drive Repository**
https://drive.google.com/drive/folders/1pOXsuKTONGsMbtgRi8e4G2EUs4zMjsw-

### 📦 Contents

Folder ini berisi berbagai hasil pengembangan dan pelatihan model yang digunakan pada HealMate AI, antara lain:

#### 🤖 Trained Models

Model deep learning yang telah dilatih untuk melakukan:

* Emotion Classification (Anxiety, Anger, Acceptance)
* Healing Score Prediction

Arsitektur yang tersedia meliputi:

* LSTM
* GRU
* CNN
* BiLSTM
* BiGRU
* BERT

#### 🏆 Best Model

Folder `best_model/` berisi model terbaik hasil evaluasi yang telah diekspor dalam format TensorFlow SavedModel dan siap digunakan untuk deployment maupun integrasi dengan REST API.

File utama:

* `saved_model.pb`
* `variables/`
* `fingerprint.pb`

#### 🔧 Model Artifacts

Folder `artifacts/` berisi komponen yang diperlukan saat proses inferensi:

* `tokenizer.pkl` → Tokenizer untuk preprocessing teks
* `label_encoder.pkl` → Encoder label emosi
* `eval_results.json` → Hasil evaluasi seluruh model
* Metadata pemilihan model terbaik

#### 📊 Training Logs

Folder `logs/` berisi TensorBoard logs dari seluruh proses training dan validasi model:

* LSTM
* GRU
* CNN
* BiLSTM
* BiGRU
* BERT

Log ini dapat digunakan untuk:

* Analisis performa training
* Monitoring loss dan accuracy
* Evaluasi potensi overfitting
* Perbandingan antar model

### 📈 Model Performance Summary

| Model  | Accuracy   | F1 Macro   | MAE Healing Score |
| ------ | ---------- | ---------- | ----------------- |
| LSTM   | 35.26%     | 17.38%     | 0.227             |
| GRU    | 47.27%     | 21.40%     | 0.233             |
| CNN    | **94.38%** | **93.51%** | 0.138             |
| BiLSTM | 92.82%     | 91.71%     | 0.116             |
| BiGRU  | 94.38%     | 93.36%     | **0.110**         |
| BERT   | 72.54%     | 69.50%     | 0.191             |

### 🏅 Selected Production Model

Berdasarkan hasil evaluasi, model **CNN** dipilih sebagai model utama untuk deployment karena memperoleh:

* Accuracy : **94.38%**
* F1 Macro : **93.51%**
* MAE Healing Score : **0.138**

Model ini digunakan sebagai dasar sistem prediksi emosi dan perhitungan Healing Score pada HealMate AI.

---

## 🏗️ Technology Stack

### Frontend

* React.js
* Vite
* JavaScript

### Backend

* FastAPI
* Python
* MongoDB
* JWT Authentication

### Data Science

* Pandas
* NumPy
* Matplotlib
* WordCloud
* Hugging Face Datasets

### Artificial Intelligence

* TensorFlow
* BERT
* LSTM
* GRU
* CNN
* BiLSTM
* BiGRU
* Gemini AI

### Deployment

* Vercel
* Railway

---

## 🛠️ Installation & Setup

### Prerequisites

* Python 3.9+
* pip

### 1. Clone Repository

```bash
git clone https://github.com/WeTeamBest/healmate_ai.git
cd healmate_ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

```bash
cp "AI/REST API/.env-example" "AI/REST API/.env"
```

Isi file `.env`:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### Cara Mendapatkan Gemini API Key

1. Buka https://aistudio.google.com/apikey
2. Login menggunakan akun Google.
3. Klik **Create API Key**.
4. Salin API Key dan masukkan ke file `.env`.

### Menjalankan REST API

```bash
cd "AI/REST API"
uvicorn main:app --reload
```

API akan berjalan pada:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## 🚀 Expected Impact

HealMate AI diharapkan dapat menjadi platform pendamping emosional yang membantu pengguna melewati proses pemulihan secara lebih sehat, terarah, dan berbasis teknologi. Dengan memadukan analisis data, kecerdasan buatan, dan pengalaman pengguna yang baik, HealMate AI tidak hanya memberikan ruang untuk bercerita, tetapi juga membantu pengguna memahami perkembangan emosional mereka secara objektif dan berkelanjutan.

---

## 📌 Conclusion

HealMate AI merupakan implementasi kolaboratif antara Full Stack Development, Data Science, dan Artificial Intelligence dalam membangun platform pemulihan emosional berbasis teknologi. Dengan memanfaatkan analisis data, deteksi emosi, prediksi Healing Score, serta integrasi Gemini AI sebagai pendamping virtual, HealMate AI mampu memberikan pengalaman dukungan emosional yang lebih personal, interaktif, dan berbasis data.

Proyek ini menunjukkan bagaimana teknologi modern dapat dimanfaatkan untuk membantu individu memahami kondisi emosional mereka, memantau proses pemulihan, serta memperoleh dukungan yang relevan kapan saja dan di mana saja.
