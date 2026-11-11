from flask import Flask, render_template, request, jsonify
import os, re, sqlite3
from datetime import datetime

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

DB = "grading.db"

def init_db():
    with sqlite3.connect(DB) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                question TEXT,
                score REAL,
                max_score REAL,
                created_at TEXT
            )
        """)

def tokenize(text):
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))

def simple_similarity(answer, key):
    a, b = tokenize(answer), tokenize(key)
    if not b:
        return 0
    return len(a & b) / len(b)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/evaluate", methods=["POST"])
def evaluate():
    student = request.form.get("student_name", "Anonymous").strip() or "Anonymous"
    question = request.form.get("question", "").strip()
    answer = request.form.get("answer", "").strip()
    key = request.form.get("answer_key", "").strip()
    max_score = float(request.form.get("max_score", 10) or 10)

    if not answer or not key:
        return jsonify({"error": "Please provide both the student answer and answer key."}), 400

    similarity = simple_similarity(answer, key)
    score = round(min(max_score, similarity * max_score), 2)

    with sqlite3.connect(DB) as con:
        con.execute(
            "INSERT INTO results(student_name, question, score, max_score, created_at) VALUES(?,?,?,?,?)",
            (student, question, score, max_score, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

    return jsonify({
        "student": student,
        "score": score,
        "max_score": max_score,
        "percentage": round((score / max_score) * 100, 1),
        "similarity": round(similarity * 100, 1),
        "message": "Evaluation completed successfully."
    })

@app.route("/api/results")
def results():
    with sqlite3.connect(DB) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute(
            "SELECT * FROM results ORDER BY id DESC LIMIT 20"
        ).fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
