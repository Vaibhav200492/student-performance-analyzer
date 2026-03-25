from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# ──────────────────────────────────────────────
# 📁  JSON Storage — data saved in students.json
# ──────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(__file__), "students.json")


def load_data():
    """Load students list from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(students):
    """Save students list to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2, ensure_ascii=False)


def next_id(students):
    """Generate next auto-increment ID."""
    return max((s["id"] for s in students), default=0) + 1


# ──────────────────────────────────────────────
# Grade Logic (same as original app.py)
# ──────────────────────────────────────────────
def calculate_grade(marks: float) -> str:
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 40:
        return "D"
    else:
        return "Fail"


# ──────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_student", methods=["POST"])
def add_student():
    data  = request.get_json()
    name  = (data.get("name") or "").strip()
    marks = data.get("marks")

    if not name:
        return jsonify({"error": "Name is required"}), 400
    try:
        marks = float(marks)
    except (TypeError, ValueError):
        return jsonify({"error": "Marks must be a number"}), 400
    if marks < 0 or marks > 100:
        return jsonify({"error": "Marks must be between 0 and 100"}), 400

    students  = load_data()
    new_id    = next_id(students)
    grade     = calculate_grade(marks)
    student   = {"id": new_id, "name": name, "marks": marks, "grade": grade}
    students.append(student)
    save_data(students)

    return jsonify(student), 201


@app.route("/students", methods=["GET"])
def get_students():
    students = load_data()
    return jsonify(list(reversed(students)))   # newest first


@app.route("/student/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    students = load_data()
    new_list = [s for s in students if s["id"] != student_id]
    if len(new_list) == len(students):
        return jsonify({"error": "Student not found"}), 404
    save_data(new_list)
    return jsonify({"message": "Deleted successfully"})


@app.route("/stats", methods=["GET"])
def get_stats():
    students = load_data()
    total    = len(students)
    average  = round(sum(s["marks"] for s in students) / total, 2) if total else 0
    topper   = max(students, key=lambda s: s["marks"], default=None)
    return jsonify({"total": total, "average": average, "topper": topper})


if __name__ == "__main__":
    app.run(debug=True)
