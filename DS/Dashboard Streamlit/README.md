# 🌿 Emotion & Healing Score Analytics Dashboard

## 📌 Project Overview
Proyek ini merupakan *dashboard* analitik interaktif yang dibangun menggunakan **Streamlit**. Aplikasi ini bertujuan untuk mengeksplorasi dan memvisualisasikan dataset emosi, serta melacak distribusi dan tren dari metrik *Healing Score*. Dashboard ini dirancang untuk memberikan *insight* yang berharga terkait pola pemulihan emosional dan analisis sentimen secara mendalam.

🔗 **Live Dashboard:** [Kunjungi Dashboard di Streamlit Cloud](https://dashboard-we-team.streamlit.app/)

## 📊 Key Features
* **Interaktif & Dinamis:** Dibekali dengan fitur penyaringan (*filtering*) agar pengguna dapat mengeksplorasi data secara spesifik.
* **Healing Score Tracking:** Visualisasi distribusi dan tren *healing score* dari berbagai rekaman data emosi.
* **Sentiment Insight:** Memetakan berbagai kategori emosi untuk mempermudah analisis pola data.

## 📂 File Structures
```text
/emotion-healing-dashboard
│
├── main.py                          # Skrip utama aplikasi Streamlit
├── Emotion Dataset Merged.xlsx      # Dataset utama yang digunakan untuk analisis
├── requirements.txt                 # Daftar library Python beserta versinya
└── README.md                        # Dokumentasi proyek
```

## Setup Environment - Anaconda
```
conda create --name healing-score-env python=3.10
conda activate healing-score-env
```

# Setup Environment - Python Venv
```
python -m venv env

# Aktivasi environment untuk Windows:
env\Scripts\activate

# Aktivasi environment untuk macOS/Linux:
source env/bin/activate
```

## Install Requirements
```
pip install -r requirements.txt
```

## Run Streamlit app
```
streamlit run main.py
```
