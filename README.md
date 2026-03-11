# ⬡ AI Smart Interview Assistant
### Resume Analyzer + Job Role Predictor + Interview Question Generator

---

## What It Does

1. **Upload** a resume (PDF or TXT)
2. **Extracts** all technical skills via NLP keyword matching
3. **Predicts** the most suitable job role using a TF-IDF + Logistic Regression model
4. **Generates** personalized interview questions (skill-based, role-based, general)
5. **Visualizes** role confidence scores with a bar chart

---

## Folder Structure

```
ai_interview_assistant/
│
├── app.py                  ← Flask backend (API + routing)
├── model.py                ← ML model training + inference
├── resume_parser.py        ← PDF/TXT parsing + skill extraction
├── question_generator.py   ← Interview question generation logic
├── dataset.csv             ← Training data (skills → job role)
├── sample_resume.txt       ← Example resume for testing
├── requirements.txt        ← Python dependencies
│
├── models/
│   └── job_classifier.pkl  ← Trained model (auto-generated on first run)
│
├── templates/
│   └── index.html          ← Frontend single-page app
│
└── static/
    └── style.css           ← Dark cyberpunk-themed stylesheet
```

---

## Quick Start

### 1. Clone / Download the project

```bash
cd ai_interview_assistant
```

### 2. Create a virtual environment (recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Pre-train the model

The model trains automatically on first use, but you can also run:

```bash
python model.py
```

This trains the classifier and saves it to `models/job_classifier.pkl`.

### 5. Run the app

```bash
python app.py
```

Open your browser at: **http://127.0.0.1:5000**

---

## Testing With the Sample Resume

A sample resume is included: `sample_resume.txt`

**Expected results:**
- Detected Role: `ML Engineer`
- Confidence: ~80–95%
- Skills: Python, TensorFlow, PyTorch, NLP, Docker, Kubernetes, AWS, etc.

---

## Supported Job Roles

| Role                | Example Skills                          |
|---------------------|------------------------------------------|
| ML Engineer         | Python, TensorFlow, PyTorch, Deep Learning |
| Data Scientist      | Python, R, Statistics, Pandas, Scikit-learn |
| Backend Developer   | Java, Spring Boot, SQL, Docker, REST API |
| Frontend Developer  | React, JavaScript, HTML, CSS, TypeScript |
| DevOps Engineer     | Docker, Kubernetes, AWS, CI/CD, Terraform |
| Full Stack Developer| React, Node.js, PostgreSQL, Docker       |
| Android Developer   | Kotlin, Android, Jetpack, Firebase       |
| Database Admin      | SQL, PostgreSQL, MongoDB, Redis          |
| QA Engineer         | Selenium, Pytest, TestNG, CI/CD          |

---

## How the ML Model Works

```
Resume Text
    ↓
Skill Extraction (regex + keyword matching)
    ↓
Skills joined as string: "Python TensorFlow Docker NLP..."
    ↓
TF-IDF Vectorizer (1–2 grams, 3000 features)
    ↓
Logistic Regression Classifier
    ↓
Predicted Role + Confidence Score
```

---

## API Endpoints

| Method | Endpoint   | Description                       |
|--------|------------|-----------------------------------|
| GET    | `/`        | Serve the frontend UI             |
| POST   | `/analyze` | Analyze uploaded resume (form-data: `resume`) |
| GET    | `/health`  | Health check                      |

---

## Extending the Project

- **Add more roles**: Add rows to `dataset.csv` and re-run `python model.py`
- **Add more skills**: Edit the `SKILL_KEYWORDS` set in `resume_parser.py`
- **Add more questions**: Add entries to `SKILL_QUESTIONS` or `ROLE_QUESTIONS` in `question_generator.py`
- **Use OpenAI**: Replace `generate_questions()` with an OpenAI API call for dynamic question generation
- **Add user accounts**: Integrate Flask-Login + SQLAlchemy to save analysis history

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| PDF shows no skills | Make sure the PDF has selectable text (not scanned) |
| Model accuracy is low | Add more rows to `dataset.csv` and retrain |
| Port 5000 in use | Run `python app.py` and change port in `app.run(port=5001)` |

---

## Tech Stack

- **Backend**: Python, Flask
- **ML**: Scikit-learn (TF-IDF + Logistic Regression)
- **NLP**: Regex + custom keyword taxonomy
- **PDF Parsing**: pdfplumber, PyPDF2
- **Frontend**: HTML5, CSS3, Vanilla JS
- **Charts**: Chart.js
- **Fonts**: Syne + JetBrains Mono (Google Fonts)
