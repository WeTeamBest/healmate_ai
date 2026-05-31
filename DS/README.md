# 🧠 Data Science Path - HealMate AI: Intelligent Post-Breakup Recovery Partner

## 📌 Project Overview
Folder Data Science (DS) ini memuat proses pengembangan dataset emosi dan *exploratory data analysis* (EDA) untuk proyek **HealMate AI**. Proyek ini bertujuan membangun sistem pendamping emosional berbasis AI untuk membantu pengguna (khususnya Generasi Z) mengelola permasalahan emosional pasca-putus cinta.

## 🗂️ Folder Structure
Struktur repositori ini dibagi menjadi beberapa direktori utama sesuai dengan alur pengerjaan:

```text
/DS
│
├── Dashboard Streamlit/
│   ├── Emotion Dataset Merged (Healing Score).xlsx
│   ├── README.md
│   ├── main.py
│   └── requirements.txt
├── Emotion Label/
│   ├── Data Dictionary.md
│   ├── Emotion Dataset Merged (Healing Score).xlsx
│   ├── Emotion Dataset Merged.xlsx
│   ├── Notebook Emotion Label.ipynb
│   ├── distribusi_emosi.png
│   ├── preprocessing_noprob.py
│   ├── wordcloud_acceptance.png
│   ├── wordcloud_anger.png
│   └── wordcloud_anxiety.png
├── Empathetic Counseling Dataset/
│   ├── Empathetic Counseling.xlsx
│   ├── Metadata Empathetic Counseling.xlsx
│   └── Notebook Empathetic Counseling.ipynb
└── CC26-PSU106 Laporan Teknis Data Scientist.pdf
```

## 🛠️ Library yang Digunakan
Proses pengolahan data menggunakan beberapa library utama, yang meliputi `pandas`, `numpy`, `re` (untuk teks preprocessing), `matplotlib`, `wordcloud`, `collections.Counter`, dan `datasets`.

## 🔍 Metodologi Pengembangan
Pengembangan dataset dikerjakan melalui dua notebook terpisah, yaitu Notebook Empathetic Counseling dan Notebook Emotion Label, untuk efisiensi komputasi sebelum akhirnya digabungkan. Tahapan utamanya meliputi:
- **Data Wrangling**: Mengumpulkan dataset emosi dari sumber publik seperti Hugging Face, Kaggle, dan Google Research.
- **Cleaning & Filtering**: Melakukan lowercase, menghapus URL, expand contractions, menghapus karakter non-alfabet, serta memfilter data menggunakan pendekatan keyword-based breakup score (contoh kata kunci: boyfriend, relationship, breakup) agar relevan dengan konteks putus cinta.
- **Feature Engineering (Emotion Lexicon)**: Mengekstrak fitur emosi dengan mengelompokkan kata ke dalam kategori Anger, Anxiety, dan Acceptance beserta bobotnya. Hal ini digunakan untuk menghitung probabilitas emosi dan menentukan label prediksi dengan batas confidence 0.34.
- **Healing Score Calculation**: Menghitung tingkat pemulihan emosional pengguna dengan mengukur keseimbangan antara emosi positif dan negatif, menggunakan formula konseptual:
``` healing_score = acceptance_prob - ((anger_prob + anxiety_prob) / 2) ```

## 📊 Key Insights (EDA)
Berdasarkan hasil visualisasi dan eksplorasi data:
- Kategori Anger mendominasi dataset dengan persentase sebesar 49,9% (2.884 teks). Emosi ini sering dikaitkan dengan kata-kata seperti hurt, rejected, dan betrayed.
- Kategori Anxiety menempati posisi kedua dengan persentase 31,0% (1.788 teks). Kategori ini sangat mencerminkan rasa kesepian dengan kemunculan kata dominan seperti lonely dan unloved.
- Kategori Acceptance memiliki porsi terkecil yaitu 19,1% (1.102 teks). Fase penerimaan ini ditandai dengan kata-kata yang berorientasi pada pemulihan diri seperti healing, better, dan myself.
