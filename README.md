# Automated Answer Sheet Checking System

A polished Flask prototype for the academic project.

## Features
- Student/question/answer-key input
- Rule-based NLP-style keyword similarity scoring
- Automatic score calculation
- SQLite evaluation history
- Responsive dashboard
- Demo data button
- Architecture prepared for OCR integration with Tesseract + OpenCV

## Run locally

1. Install Python 3.10+.
2. Open a terminal in this folder.
3. Run:
   `pip install -r requirements.txt`
4. Start:
   `python app.py`
5. Open:
   `http://127.0.0.1:5000`

## OCR integration
The current interface accepts text so it works immediately. For the full project, add an `/ocr` endpoint using `pytesseract` and OpenCV to process uploaded scanned answer sheets, then pass the extracted text into `/evaluate`.

## Important grading note
The demo scoring is intentionally simple keyword-overlap scoring. For a research/project implementation, combine TF-IDF/cosine similarity, rubric-weighted keywords, sentence embeddings, and teacher review for edge cases rather than treating automated similarity as a definitive assessment.
