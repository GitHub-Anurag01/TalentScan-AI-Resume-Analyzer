# app.py
# -------------------------------------------------------
# Flask backend for AI Smart Interview Assistant.
#
# Endpoints:
#   GET  /               — Serve the single-page UI
#   POST /analyze        — Analyze uploaded resume
#   GET  /health         — Health check
# -------------------------------------------------------

import os
import json
import traceback
from flask import Flask, request, jsonify, render_template, send_from_directory

from resume_parser import parse_resume
from model import load_model, predict
from question_generator import generate_questions

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB upload limit

# Allowed extensions
ALLOWED_EXTENSIONS = {"pdf", "txt", "doc"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Pre-load model at startup so the first request isn't slow
print("[App] Pre-loading ML model …")
_model = load_model()
print("[App] Model ready.")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the main single-page application."""
    return render_template("index.html")


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "model_loaded": _model is not None})


@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Main analysis endpoint.

    Expects: multipart/form-data with field 'resume' (PDF or TXT file).

    Returns JSON:
    {
        "success": bool,
        "skills": [...],
        "job_role": "...",
        "confidence": 0.95,
        "all_scores": [{"role": "...", "score": 0.95}, ...],
        "questions": {
            "skill_based": [...],
            "role_based": [...],
            "general": [...]
        },
        "contact": {...},
        "word_count": 350,
        "error": "..." (only on failure)
    }
    """
    # --- Validate request ---
    if "resume" not in request.files:
        return jsonify({"success": False, "error": "No file uploaded. Please attach a resume."}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": f"Unsupported file type. Please upload a PDF or TXT file."
        }), 400

    try:
        # --- Parse resume ---
        file_bytes = file.read()
        parsed     = parse_resume(file_bytes, file.filename)

        skills     = parsed["skills"]
        text       = parsed["text"]
        contact    = parsed["contact"]
        word_count = parsed["word_count"]

        if not skills:
            # If no skills matched, still attempt role prediction on raw text
            skills = []

        # --- Predict job role ---
        prediction = predict(skills, _model)
        job_role   = prediction["job_role"]
        confidence = prediction["confidence"]
        all_scores = prediction["all_scores"][:5]  # Top 5 roles

        # --- Generate interview questions ---
        questions = generate_questions(skills, job_role, num_questions=8)

        # --- Return results ---
        return jsonify({
            "success":    True,
            "skills":     skills,
            "job_role":   job_role,
            "confidence": confidence,
            "all_scores": all_scores,
            "questions":  questions,
            "contact":    contact,
            "word_count": word_count,
        })

    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 422

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred while processing your resume.",
            "detail": str(e)
        }), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  AI Smart Interview Assistant")
    print("  http://127.0.0.1:5000")
    print("="*55 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
