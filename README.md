# 🚀 AI Resume Skill Gap Classifier

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14%2B-black.svg)](https://nextjs.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-yellow.svg)](https://mlflow.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent, full-stack system that automates resume screening and skill gap analysis. By leveraging NLP and Machine Learning on the backend, and a modern Next.js dashboard on the frontend, it maps candidate resume skills against job requirements, classifies the match level, and provides actionable, curated upskilling recommendations.

> 💡 **Note:** The frontend of this project was bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app) and utilizes [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load the [Geist](https://vercel.com/font) font family.

---

## 📋 Table of Contents
- [Executive Summary](#executive-summary)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-endpoints)
- [Machine Learning Pipeline Details](#machine-learning-pipeline-details)
- [Future Roadmap](#future-roadmap)
- [License](#license)

---

## 🎯 Executive Summary
Recruiters spend ~30% of their time on manual resume screening, leading to inefficiency, inconsistency, and a lack of constructive feedback for candidates. This project solves that by providing:
1. **Automated Screening**: Reduces time-to-screen from minutes to under 500ms.
2. **Explainable AI**: Outputs specific missing and matched skills to justify predictions.
3. **Actionable Feedback**: Provides candidates with curated, free learning resources to bridge identified skill gaps.

### Target Classification Labels
- 🟢 **Strong Match**: >90% of required skills met. *(Fast-track to interview)*
- 🟡 **Moderate Match**: 60-90% of required skills met. *(Phone screen recommended)*
- 🟠 **Skill Gap**: 30-60% of required skills met. *(Redirect to junior roles)*
- 🔴 **High Skill Gap**: <30% of required skills met. *(Auto-reject with feedback)*

---

## ✨ Key Features
- 📄 **Multi-Format Parsing**: Extracts and cleans text from `.pdf`, `.docx`, and `.txt` files.
- 🧠 **Smart NLP Extraction**: Regex-based skill extraction with a comprehensive synonym-mapping engine (e.g., "ml" → "machine learning", "gcp" → "google cloud").
- 📊 **Advanced Feature Engineering**: Computes Jaccard Similarity, Cosine Similarity (TF-IDF), Missing Skill Count, and Exact Match Ratio.
- 🤖 **High-Accuracy Modeling**: `GradientBoostingClassifier` optimized via `GridSearchCV` and tracked with **MLflow**.
- 🎓 **Curated Learning Paths**: Recommends top-tier, free learning resources for missing skills.
- 🔐 **Full-Stack Dashboard**: A modern Next.js UI featuring user authentication, drag-and-drop file uploads, circular progress match scores, and local analysis history.

---

## 🛠️ Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Backend & API** | Python, FastAPI, Uvicorn, Pydantic |
| **Machine Learning** | Scikit-Learn, Pandas, NumPy, Joblib |
| **NLP & Parsing** | `pdfminer.six`, `python-docx`, Regex |
| **Experiment Tracking**| MLflow |
| **Frontend** | Next.js (App Router), React, TypeScript, Tailwind CSS |
| **UI/UX** | Lucide React Icons, Geist Font, Custom Dark Mode |
| **Testing** | Pytest, HTTPX |

---

## 📂 Project Structure

```text
skill_gap_classifier/
├── src/
│   ├── config.py                      # Skill taxonomy, synonyms, learning resources, paths
│   ├── data/
│   │   └── generate_data.py           # Synthetic balanced dataset generation
│   ├── parsing/
│   │   ├── document_parser.py         # PDF/TXT text extraction and noise cleaning
│   │   └── job_parser.py              # Job description specific boilerplate removal
│   ├── extraction/
│   │   └── skill_extractor.py         # Regex-based skill extraction with synonym mapping
│   ├── features/
│   │   └── feature_builder.py         # TF-IDF, Jaccard, Cosine, Exact Match Ratio engineering
│   ├── modeling/
│   │   ├── train.py                   # GradientBoosting with GridSearchCV & MLflow
│   │   └── evaluate_model.py          # Confusion matrix and classification report generation
│   ├── recommendations/
│   │   └── recommender.py             # Maps missing skills to curated learning resources
│   └── pipelines/
│       └── inference_pipeline.py      # End-to-end prediction orchestration
├── api/
│   └── app.py                         # FastAPI application with CORS and Auth endpoints
├── frontend/                          # Next.js application directory
│   ├── app/
│   │   ├── globals.css                # Tailwind setup with dark mode
│   │   ├── layout.tsx                 # Root layout with Geist fonts
│   │   └── page.tsx                   # Main Dashboard (Auth, Analyzer, Results, History)
│   └── package.json
├── models/                            # Saved .joblib artifacts and confusion_matrix.png
├── data/
│   └── processed/                     # Generated training_data.csv
├── mlruns/                            # MLflow experiment tracking directory
├── setup.py                           # Project metadata and packaging
└── README.md
```

---

## ⚙️ Prerequisites
- **Python**: 3.9 or higher
- **Node.js**: 18.x or higher
- **Package Managers**: `pip` (or `poetry`), `npm` (or `yarn`/`pnpm`/`bun`)

---

## 🚀 Installation & Setup

### 1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/your-username/skill_gap_classifier.git
cd skill_gap_classifier

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -e .
```

2. Frontend Setup
```bash
cd frontend

# Install Node dependencies
npm install
# or yarn install / pnpm install / bun install
```

## 💻 Usage Guide

## Step 1: Generate Synthetic Training Data
Create a balanced dataset for the 4 classification labels.
```bash
python -m src.data.generate_data
```

## Step 2: Train the Machine Learning Model
Train the Gradient Boosting model, tune hyperparameters, and log metrics to MLflow.
```bash
python -m src.modeling.train
```

## (Optional) View MLflow UI to track experiments:
```bash
mlflow ui
# Open http://localhost:5000 in your browser
```

## Step 3: Evaluate the Model
Generate a classification report and save a confusion matrix.
```bash
python -m src.modeling.evaluate_model
```

## Step 4: Start the FastAPI Backend
```bash
# From the project root directory
uvicorn api.app:app --reload
# API will be available at http://localhost:8000
# Swagger Docs at http://localhost:8000/docs
```

## Step 5: Start the Next.js Frontend
Open a new terminal, navigate to the frontend folder, and run the development server:
```bash
cd frontend
npm run dev
# or yarn dev, pnpm dev, bun dev
```
Open http://localhost:3000 with your browser to see the result. You can start editing the page by modifying frontend/app/page.tsx. The page auto-updates as you edit the file.

## 🔌 API Endpoints

| Method | Endpoint | Description | Payload / Params |
| :---: | :--- | :--- | :--- |
| `POST` | `/auth/signup` | Register a new user | `{"email": "string", "password": "string"}` |
| `POST` | `/auth/login` | Authenticate user | `{"email": "string", "password": "string"}` |
| `POST` | `/predict` | Analyze resume vs JD | **FormData:** `resume` (File), `job_description` (String) |

## Example /predict Response:
```json
{
  "prediction": "Moderate Match",
  "match_score": 75,
  "gap_percentage": 25,
  "match_level": "Moderate Match",
  "resume_skills": ["python", "sql", "pandas"],
  "jd_skills": ["python", "sql", "pandas", "docker", "aws"],
  "matching_skills": ["pandas", "python", "sql"],
  "missing_skills": ["aws", "docker"],
  "learning_resources": [
    {
      "skill": "docker",
      "resources": [
        {"title": "Docker Curriculum", "url": "https://docker-curriculum.com/", "type": "Tutorial"}
      ]
    }
  ]
}
```


## 🧠 Machine Learning Pipeline Details
1. Data Generation: Creates synthetic resume/JD pairs with controlled overlap percentages to ensure balanced classes.
2. Text Cleaning: Removes boilerplate, normalizes case, and preserves critical tech symbols (e.g., C++, .NET, C#).
3. Skill Extraction: Uses a compiled, length-sorted Regex pattern to find skills, immediately mapping variations (e.g., "k8s" → "kubernetes") to a master SKILL_TAXONOMY.
4. Feature Engineering:
- Jaccard Similarity: Intersection over Union of skill sets.
- Cosine Similarity: TF-IDF vector similarity between resume and JD text.
- Exact Match Ratio: Percentage of required job skills present in the resume.
- Missing Count: Absolute number of required skills absent.
5. Modeling: GradientBoostingClassifier with 5-fold cross-validated GridSearchCV to maximize accuracy.

## 🗺️ Future Roadmap
1. OCR Integration: Add support for image-based or scanned resumes using Tesseract or AWS Textract.
2. Real Database: Replace in-memory authentication with PostgreSQL and hashed passwords (bcrypt).
3. LLM Enhancement: Integrate a lightweight LLM (e.g., Llama 3 via Ollama) for semantic skill matching beyond strict keyword/regex matching.
4. CI/CD Pipeline: Add GitHub Actions for automated testing (pytest) and linting.
5. Dockerization: Add Dockerfile and docker-compose.yml for one-click, containerized deployment.

## 📜 License & Deployment
This project is licensed under the MIT License. 

## If you found this project helpful, please consider giving it a ⭐ on GitHub!
