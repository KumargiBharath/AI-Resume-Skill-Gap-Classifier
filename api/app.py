import sys
import os
import shutil  
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import BaseModel  # NEW IMPORT

# 10
# To Run:"uvicorn api.app:app --reload"
# Setup Loguru
logger.remove()
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipelines.inference_pipeline import SkillGapPredictor
from src.parsing.document_parser import DocumentParser

# -------------------------------------------------------
# APP SETUP
# -------------------------------------------------------
app = FastAPI(
    title="AI Resume Skill Gap Classifier API",
    description="Production-Grade API to classify skill gaps.",
    version="3.0"
)

# CORS Setup (Required for Next.js)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------
# AUTH SETUP (NEW)
# -------------------------------------------------------
# --- Simple User DB (In-Memory) ---
# In production, replace this with a real database
fake_users_db = {}

class UserAuth(BaseModel):
    email: str
    password: str

# --- Auth Endpoints ---
@app.post("/auth/signup")
async def sign_up(user: UserAuth):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    # NOTE: In production, HASH the password!
    fake_users_db[user.email] = {"email": user.email, "password": user.password}
    return {"message": "User created successfully"}

@app.post("/auth/login")
async def log_in(user: UserAuth):
    db_user = fake_users_db.get(user.email)
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"message": "Login successful", "email": user.email}

# -------------------------------------------------------
# MODEL LOADING
# -------------------------------------------------------

# Load model
try:
    logger.info("Initializing Model...")
    predictor = SkillGapPredictor()
    logger.info("Model Loaded.")
except Exception as e:
    logger.error(f"CRITICAL: Model failed to load: {e}")
    predictor = None

# Constants
MAX_FILE_SIZE_MB = 5

# -------------------------------------------------------
# CORE ENDPOINTS
# -------------------------------------------------------
@app.get("/")
def home():
    return {"status": "ok", "message": "API is running."}

@app.post("/predict")
async def predict_from_files(
    resume: UploadFile = File(..., description="Resume File (PDF or TXT)"),
    job_description: str = Form(..., description="Job Description Text")
):
    if not predictor:
        raise HTTPException(status_code=500, detail="Model not loaded.")

    # REVERTED: Strictly PDF and TXT as per your original code
    if not resume.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
    
    file_size = 0
    temp_path = f"temp_{resume.filename}"
    
    try:
        logger.info(f"Processing file: {resume.filename}")
        
        with open(temp_path, "wb") as buffer:
            for chunk in iter(lambda: resume.file.read(1024 * 1024), b''):
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE_MB * 1024 * 1024:
                    os.remove(temp_path)
                    raise HTTPException(status_code=413, detail=f"File too large. Limit is {MAX_FILE_SIZE_MB}MB.")
                buffer.write(chunk)
        
        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job Description cannot be empty.")

        parser = DocumentParser()
        resume_text = parser.parse(temp_path)
        
        if not resume_text:
            raise HTTPException(status_code=400, detail="Could not extract text from resume.")

        # Call your ML Pipeline
        result = predictor.predict(resume_text, job_description)
        
        # -------------------------------------------------------
        # ENRICHMENT FOR FRONTEND
        # -------------------------------------------------------
        
        # The pipeline returns 'match_percentage', we map it to 'match_score' (int) for the circular progress bar
        match_score = int(result.get("match_percentage", 0))
        gap_percentage = 100 - match_score
        
        # Determine Match Level Text
        if match_score >= 80:
            match_level = "Highly and Strong Match"
        elif match_score >= 50:
            match_level = "Moderate Match"
        else:
            match_level = "Less Match"

        # Add these fields to the result dictionary for the frontend
        result["match_score"] = match_score
        result["gap_percentage"] = gap_percentage
        result["match_level"] = match_level
        
        logger.info(f"Prediction complete: {result['prediction']}")
        return result

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)