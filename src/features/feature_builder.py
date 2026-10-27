import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys
from loguru import logger

# 5
#ToRun:"python -m src.features.feature_builder"

# -------------------------------------------------------
# SETUP LOGURU
# -------------------------------------------------------
# Remove the default handler to prevent duplicate logs
logger.remove()
# Add a new handler with a custom format and colors
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

# Add path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.config import DATA_DIR

class FeatureEngineer:
    """
    Transforms lists of skills into numerical feature vectors.
    """
    def __init__(self):
        logger.info("Initializing FeatureEngineer...")
        # Initialize a TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer()

    def fit(self, resume_skills_list, job_skills_list):
        """
        Learns the vocabulary from all skills.
        """
        logger.info("Fitting vectorizer on skill corpus...")
        resume_corpus = [" ".join(skills) if isinstance(skills, list) else skills for skills in resume_skills_list]
        job_corpus = [" ".join(skills) if isinstance(skills, list) else skills for skills in job_skills_list]
        
        all_text = resume_corpus + job_corpus
        self.vectorizer.fit(all_text)
        logger.info(f"Vectorizer fitted. Vocabulary size: {len(self.vectorizer.vocabulary_)}")

    def transform(self, resume_skills_list, job_skills_list):
        """
        Converts skill lists to feature vectors.
        """
        logger.info(f"Transforming {len(resume_skills_list)} samples...")
        features = []
        
        resume_corpus = [" ".join(skills) if isinstance(skills, list) else skills for skills in resume_skills_list]
        job_corpus = [" ".join(skills) if isinstance(skills, list) else skills for skills in job_skills_list]
        
        resume_vecs = self.vectorizer.transform(resume_corpus)
        job_vecs = self.vectorizer.transform(job_corpus)

        # Calculate Cosine Similarity
        cos_sims = np.diagonal(cosine_similarity(resume_vecs, job_vecs))

        for i in range(len(resume_skills_list)):
            r_skills = resume_skills_list[i] if isinstance(resume_skills_list[i], list) else resume_skills_list[i].split()
            j_skills = job_skills_list[i] if isinstance(job_skills_list[i], list) else job_skills_list[i].split()
            
            resume_set = set(r_skills)
            job_set = set(j_skills)
            
            intersection = len(resume_set.intersection(job_set))
            union = len(resume_set.union(job_set))
            
            # --- FEATURE ENGINEERING UPGRADE ---
            
            # Feature 1: Jaccard Similarity (Old)
            jaccard = intersection / union if union > 0 else 0
            
            # Feature 2: Missing Skill Count (Old)
            missing_count = len(job_set - resume_set)
            
            # Feature 3: Cosine Similarity (Old)
            cos_sim = cos_sims[i]
            
            # Feature 4: Exact Match Ratio (NEW - CRITICAL)
            # This ignores 'noise' skills and focuses purely on Job Requirements met
            exact_match_ratio = intersection / len(job_set) if job_set else 0
            
            features.append([jaccard, missing_count, cos_sim, exact_match_ratio])
        
        logger.info("Transformation complete.")
        return np.array(features)

# --- Test Block ---
if __name__ == "__main__":
    logger.info("[Phase 8 Test] Loading Data...")
    
    csv_path = os.path.join(DATA_DIR, "processed", "training_data.csv")
    df = pd.read_csv(csv_path)
    
    df['resume_skills'] = df['resume_skills'].fillna("")
    df['job_skills'] = df['job_skills'].fillna("")
    
    resume_lists = [s.split(", ") if s else [] for s in df['resume_skills']]
    job_lists = [s.split(", ") if s else [] for s in df['job_skills']]
    
    fe = FeatureEngineer()
    
    logger.info("[Phase 8 Test] Fitting Vectorizer...")
    fe.fit(resume_lists, job_lists)
    
    logger.info("[Phase 8 Test] Transforming features...")
    X = fe.transform(resume_lists, job_lists)
    
    logger.info(f"Shape of Feature Matrix: {X.shape}") # Should now be (1400, 4)
    logger.info(f"First 5 Feature Vectors:\n{X[:5]}")
    logger.info("[SUCCESS] Phase 8 Feature Engineering Upgraded!")