import joblib
import os
import sys
import numpy as np
import argparse
import json
from loguru import logger

# -------------------------------------------------------
# SETUP LOGURU
# -------------------------------------------------------
logger.remove()
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config import MODEL_DIR, CLASS_LABELS
from src.parsing.document_parser import DocumentParser
from src.parsing.job_parser import JobParser
from src.extraction.skill_extractor import SkillExtractor
from src.features.feature_builder import FeatureEngineer
from src.recommendations.recommender import ResourceRecommender

class SkillGapPredictor:
    def __init__(self):
        logger.info("[Inference] Loading model artifacts...")
        
        # 1. Load Model and Feature Engineer
        model_path = os.path.join(MODEL_DIR, "skill_gap_model.joblib")
        fe_path = os.path.join(MODEL_DIR, "feature_engineer.joblib")
        
        if not os.path.exists(model_path) or not os.path.exists(fe_path):
            logger.error("Model files not found. Please run training first.")
            raise FileNotFoundError("Model files not found. Please run training first.")

        self.model = joblib.load(model_path)
        self.fe = joblib.load(fe_path)
        
        # 2. Initialize Parsers and Extractors
        self.resume_parser = DocumentParser()
        self.job_parser = JobParser()
        self.skill_extractor = SkillExtractor()
        
        # Initialize Recommender
        self.recommender = ResourceRecommender()
        
        logger.info("[Inference] System ready.")

    def predict(self, resume_text: str, job_text: str):
        logger.info("Starting prediction process...")
        
        # 1. Clean
        clean_resume = self.resume_parser.clean_text(resume_text)
        clean_job = self.job_parser.clean_text(job_text)
        
        # 2. Extract
        resume_skills = self.skill_extractor.extract(clean_resume)
        job_skills = self.skill_extractor.extract(clean_job)
        
        # 3. Features
        features = self.fe.transform([resume_skills], [job_skills])
        
        # 4. Predict
        prediction_idx = self.model.predict(features)[0]
        prediction_label = CLASS_LABELS[prediction_idx]
        
        # 5. Missing Skills & Matching Skills
        resume_set = set(resume_skills)
        job_set = set(job_skills)
        
        missing_skills = list(job_set - resume_set)
        
        # *** NEW: Calculate Matching Skills for Frontend ***
        matching_skills = list(job_set.intersection(resume_set))
        
        # Calculate match based on intersection (actual overlap)
        match_percentage = round((len(matching_skills) / len(job_skills)) * 100, 2) if job_skills else 0
        
        # 6. Get Recommendations
        recommendations = self.recommender.get_recommendations(missing_skills)
        
        logger.info(f"Prediction complete: {prediction_label} (Match: {match_percentage}%)")
        
        # *** RETURN: Keys updated for Next.js Frontend compatibility ***
        return {
            "prediction": prediction_label,
            "resume_skills": sorted(resume_skills),
            "jd_skills": sorted(job_skills),            # RENAMED from 'required_skills'
            "missing_skills": sorted(missing_skills),
            "matching_skills": sorted(matching_skills), # ADDED for Frontend
            "match_percentage": match_percentage,
            "learning_resources": recommendations       # RENAMED from 'recommended_resources'
        }

if __name__ == "__main__":
    # --- DYNAMIC INPUT HANDLING ---
    
    parser = argparse.ArgumentParser(description="Run Skill Gap Inference")
    parser.add_argument("--resume", type=str, help="Path to the resume file (PDF or TXT)")
    parser.add_argument("--jd", type=str, help="Path to the job description file (TXT)")
    args = parser.parse_args()

    predictor = SkillGapPredictor()

    # Check if user provided files
    if args.resume and args.jd:
        logger.info(f"[Input] Using Resume: {args.resume}")
        logger.info(f"[Input] Using JD: {args.jd}")
        
        # Extract text from the provided files
        doc_parser = DocumentParser()
        
        resume_text = doc_parser.parse(args.resume)
        
        # For JD, we assume it's text, so we just read it
        with open(args.jd, 'r', encoding='utf-8') as f:
            jd_text = f.read()
            
        output = predictor.predict(resume_text, jd_text)
        
    else:
        # Fallback to dummy data if no arguments provided
        logger.info("[Input] No files provided. Running with Dummy Data...")
        dummy_resume = """
        John Doe
        Skills: Python, Pandas, Scikit-Learn, SQL, Machine Learning.
        """
        dummy_jd = """
        Data Scientist Role.
        Required Skills: Python, Deep Learning, Tensorflow, SQL, Docker, NLP.
        """
        output = predictor.predict(dummy_resume, dummy_jd)

    # Print the result
    logger.info("--- PREDICTION RESULTS ---")
    print(json.dumps(output, indent=2))