# resume_parser.py
# -------------------------------------------------------
# Handles PDF and plain-text resume parsing.
# Extracts raw text, then identifies skills using a
# comprehensive keyword dictionary.
# -------------------------------------------------------

import re
import io

# ---------------------------------------------------------------------------
# Comprehensive skill taxonomy — extend as needed
# ---------------------------------------------------------------------------
SKILL_KEYWORDS = {
    # Languages
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C",
    "Go", "Rust", "Ruby", "Swift", "Kotlin", "PHP", "Scala", "R",
    "MATLAB", "Perl", "Bash", "Shell", "Dart", "Lua",

    # Web Frontend
    "HTML", "CSS", "React", "Angular", "Vue.js", "Vue", "Next.js",
    "Nuxt.js", "Svelte", "jQuery", "Bootstrap", "Tailwind", "SASS",
    "SCSS", "Webpack", "Vite", "Redux", "MobX",

    # Web Backend / Frameworks
    "Node.js", "Express", "Django", "Flask", "FastAPI", "Spring",
    "Spring Boot", "Rails", "Laravel", "ASP.NET", ".NET", "Hibernate",
    "Maven", "Gradle",

    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis",
    "Cassandra", "DynamoDB", "Oracle", "Neo4j", "Elasticsearch",
    "Firebase", "Firestore", "MariaDB",

    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes",
    "Terraform", "Ansible", "Jenkins", "CI/CD", "GitHub Actions",
    "GitLab CI", "CircleCI", "Helm", "Nginx", "Apache",

    # Data Science & ML
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "Data Science", "Statistics", "Data Analysis", "Data Visualization",
    "Feature Engineering", "Model Deployment",

    # ML Libraries
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas",
    "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly", "XGBoost",
    "LightGBM", "CatBoost", "Hugging Face", "Transformers", "BERT",
    "GPT", "OpenCV", "NLTK", "spaCy", "Gensim", "MLflow", "Airflow",
    "Spark", "Hadoop", "Kafka",

    # Mobile
    "Android", "iOS", "React Native", "Flutter", "Xcode", "Android Studio",
    "Jetpack Compose", "SwiftUI",

    # Other Tools & Practices
    "REST API", "GraphQL", "Microservices", "Agile", "Scrum",
    "Git", "GitHub", "GitLab", "Bitbucket", "JIRA", "Confluence",
    "Linux", "Unix", "Windows Server", "OOP", "Design Patterns",
    "SOLID", "TDD", "BDD", "Selenium", "Pytest", "JUnit", "TestNG",
    "Postman", "Swagger", "OpenAPI", "RabbitMQ", "gRPC",
}

# Lowercase version for fast matching
_SKILL_LOWER = {s.lower(): s for s in SKILL_KEYWORDS}


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract all text from a PDF given its raw bytes.
    Tries pdfplumber first (better layout); falls back to PyPDF2.

    Args:
        file_bytes: Raw bytes of the uploaded PDF file.

    Returns:
        Extracted text as a single string.
    """
    text = ""

    # --- Attempt 1: pdfplumber (preferred) ---
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if text.strip():
            return text
    except Exception:
        pass

    # --- Attempt 2: pypdf (newer, widely available) ---
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():
            return text
    except Exception:
        pass

    # --- Attempt 3: PyPDF2 (legacy fallback) ---
    # Try the older PyPDF2 package in case pypdf/pdfplumber aren't
    # available.  This used to be the main library before the project
    # was renamed, so many environments still have it installed.
    try:
        # note: `PyPDF2` provides the same PdfReader interface as pypdf
        from PyPDF2 import PdfReader as LegacyPdfReader
        reader = LegacyPdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        # if we reach this point none of the PDF libraries were usable
        # raise a ValueError so the calling code can generate a user-
        # friendly error message instead of an internal 500.
        raise ValueError(f"Could not extract text from PDF: {e}")

    return text


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode plain-text resume bytes to a string."""
    for encoding in ("utf-8", "latin-1", "cp1252"):
        try:
            return file_bytes.decode(encoding)
        except UnicodeDecodeError:
            continue
    return file_bytes.decode("utf-8", errors="replace")


def extract_skills(text: str) -> list:
    """
    Scan resume text for known skill keywords.

    Uses word-boundary regex matching so 'C' doesn't match inside 'CSS'.
    Returns a deduplicated list of matched canonical skill names.

    Args:
        text: The raw resume text.

    Returns:
        Sorted list of detected skill strings.
    """
    text_lower = text.lower()
    found = set()

    for skill_lower, skill_canonical in _SKILL_LOWER.items():
        # Use word-boundary regex for accuracy
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill_canonical)

    return sorted(found)


def extract_contact_info(text: str) -> dict:
    """
    Extract basic contact information from resume text.

    Returns:
        Dict with 'email', 'phone', 'linkedin', 'github' keys.
    """
    info = {}

    # Email
    email_match = re.search(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text
    )
    info["email"] = email_match.group() if email_match else None

    # Phone
    phone_match = re.search(
        r'(\+?\d[\d\s\-().]{7,}\d)', text
    )
    info["phone"] = phone_match.group().strip() if phone_match else None

    # LinkedIn
    linkedin_match = re.search(
        r'linkedin\.com/in/[\w\-]+', text, re.IGNORECASE
    )
    info["linkedin"] = linkedin_match.group() if linkedin_match else None

    # GitHub
    github_match = re.search(
        r'github\.com/[\w\-]+', text, re.IGNORECASE
    )
    info["github"] = github_match.group() if github_match else None

    return info


def parse_resume(file_bytes: bytes, filename: str) -> dict:
    """
    Main entry point: parse a resume file and return structured data.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        filename  : Original filename (used to detect PDF vs text).

    Returns:
        Dict containing 'text', 'skills', 'contact', 'word_count'.
    """
    filename_lower = filename.lower()

    if filename_lower.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    else:
        text = extract_text_from_txt(file_bytes)

    if not text.strip():
        raise ValueError("No text could be extracted from the uploaded file.")

    skills = extract_skills(text)
    contact = extract_contact_info(text)
    word_count = len(text.split())

    return {
        "text": text,
        "skills": skills,
        "contact": contact,
        "word_count": word_count,
    }
