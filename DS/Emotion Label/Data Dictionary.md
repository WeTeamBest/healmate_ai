# Data Dictionary (Emotion Label Dataset)
## Dataset
1. 'Emotion Label Dataset.xlsx': data label emosi yang dihasilkan dari sumber label emotion.
2. 'Emotion Dataset Merged.xlsx': data label emosi hasil penggabungan antara `Emotion Label Dataset` dengan `Empathetic Counseling`.

## Kolom
- `text_clean_v1`: teks yang telah dibersihkan tanpa menghapus tanda baca seperti titik (.), koma(,), dan sebagainya.
- `text_clean_v2`: teks yang telah dibersihkan, termasuk menghapus tanda baca seperti titik (.), koma(,), dan sebagainya.
- `anger_prob`: probabilitas suatu teks tergolong dalam emosi `anger`.
- `anxiety_prob`: probabilitas suatu teks tergolong dalam emosi `anxiety`.
- `acceptance_prob`: probabilitas suatu teks tergolong dalam emosi `acceptance`.
- `predicted_emotion`: emosi yang paling dominan, dilihat dari probabilitas emosi terbesar.
- `emotion_confidence`: tingkat keyakinan suatu teks tersebut tergolong ke dalam emosi pada `predicted_emotion`.
