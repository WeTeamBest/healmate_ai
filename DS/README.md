# 🧠 Data Science Path - HealMate AI: Intelligent Post-Breakup Recovery Partner

## **Latar Belakang**
Proyek **HealMate AI** dikembangkan untuk menjadi sistem pendamping emosional berbasis AI guna membantu pengguna (khususnya Generasi Z) mengelola permasalahan dan fase krisis pasca-putus cinta. Pada *learning path* Data Science, fokus utamanya adalah mengkurasi dataset teks, melakukan analisis sentimen, serta merumuskan metrik pemulihan emosional (*Healing Score*) agar AI dapat merespons pengguna secara empatik dan terukur.

## **Import Library**
Dalam proses pengolahan data, berbagai library Python digunakan untuk efisiensi komputasi:
* `pandas` & `numpy`: Manipulasi data tabular dan komputasi numerik.
* `re`: *Regular expressions* untuk *text preprocessing* dan pembersihan karakter.
* `matplotlib` & `wordcloud`: Pembuatan visualisasi data dan distribusi kata.
* `collections.Counter`: Perhitungan frekuensi kemunculan kata spesifik.
* `datasets`: Mengunduh dataset publik dari repositori Hugging Face.

## **Struktur Notebook Pengembangan Data Scientist**
Untuk mengoptimalkan efisiensi komputasi dan memori, proses pengembangan (*pipeline*) dibagi menjadi dua *notebook* terpisah sebelum data akhirnya digabungkan:
1. **Notebook Empathetic Counseling:** Berfokus pada pengumpulan, pembersihan, dan pemrosesan awal dari dataset dialog konseling.
2. **Notebook Emotion Label:** Berfokus pada proses penentuan pelabelan emosi menggunakan pendekatan leksikon (*lexicon-based*) dan kalkulasi *Healing Score*.

## ***Data Wrangling***
Proses ini mencakup pengumpulan dataset sekunder dari berbagai sumber publik yang kredibel (seperti Hugging Face, Kaggle, dan Google Research). Data mentah ini terdiri dari teks percakapan konseling, curhatan (*ranting*), dan ekspresi emosi yang kemudian disatukan ke dalam satu format kerangka data (DataFrame).

## ***Cleaning Dataset***
Tahapan krusial untuk memastikan model AI belajar dari data yang berkualitas:
* **Text Preprocessing Dasar:** Mengubah seluruh teks menjadi *lowercase*, menghapus tautan (URL), melakukan *expand contractions* (misal: *don't* menjadi *do not*), dan menghapus karakter non-alfabet.
* **Context Filtering (Breakup Score):** Menyaring dataset ekstensif dengan teknik *keyword-based* (contoh kata kunci: *boyfriend, relationship, breakup, hurt*). Teks yang tidak memenuhi batas minimum *score* relevansi putus cinta akan dibuang agar konteks data tetap spesifik.

## ***EDA & Data Visualization***
Mengeksplorasi dan mengekstrak fitur emosi (*Anger, Anxiety, Acceptance*) beserta bobot probabilitasnya. Dari visualisasi (seperti *Pie Chart* dan *Wordcloud*), diperoleh *insight* berikut:
* **Anger (49,9% | 2.884 teks):** Mendominasi dataset. Kata yang paling sering muncul antara lain *hurt, rejected, betrayed*.
* **Anxiety (31,0% | 1.788 teks):** Mencerminkan rasa kesepian dan kekhawatiran dengan kemunculan kata seperti *lonely, unloved*.
* **Acceptance (19,1% | 1.102 teks):** Fase pemulihan dengan kata-kata orientasi perbaikan diri seperti *healing, better, myself*.
* **Healing Score Logic:** Tingkat pemulihan dihitung dari keseimbangan emosi positif dan negatif menggunakan formula konseptual:
  `healing_score = acceptance_prob - ((anger_prob + anxiety_prob) / 2)`

## **Export Dataset**
Setelah seluruh teks bersih, dilabeli dengan kategori emosi (dengan batas *confidence* 0.34), dan dihitung *Healing Score*-nya, dataset hasil akhir (*Merged*) diekspor ke dalam format `.xlsx` dan `.csv`. Data terstruktur ini adalah produk akhir yang siap disuntikkan ke proses *Machine Learning Training* dan *Dashboard Streamlit*.

## **Kesimpulan**
Tim Data Science telah berhasil membangun dan mengkurasi dataset spesifik untuk konteks *post-breakup recovery*. Melalui otomatisasi pelabelan *lexicon-based* dan penyaringan kata kunci, dataset yang dihasilkan memiliki relevansi konteks yang sangat tinggi. Perumusan metrik *Healing Score* juga terbukti selaras dengan distribusi emosi (dari fase marah, cemas, hingga penerimaan), menjadikan dataset ini pondasi yang sangat ideal untuk membangun kecerdasan HealMate AI.
