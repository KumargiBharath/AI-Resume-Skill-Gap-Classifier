import pandas as pd
import numpy as np
import random
import os
import sys
from loguru import logger

# 1
#To Run:"python -m src.data.generate_data"

# -------------------------------------------------------
# SETUP LOGURU
# -------------------------------------------------------
# Remove the default handler to prevent duplicate logs
logger.remove()
# Add a new handler with a custom format and colors
# format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}"
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.config import SKILL_TAXONOMY, CLASS_LABELS, DATA_DIR

def generate_balanced_data(n_samples_per_class=300):
    """
    Generates a balanced dataset by creating specific examples
    for each class type.
    """
    data = []
    total_samples = n_samples_per_class * 4
    logger.info(f"[Phase 4] Generating {total_samples} BALANCED synthetic data samples...")

    # Helper to generate skills based on desired overlap
    def create_sample(target_label):
        # 1. Pick Job Skills (Requirements)
        num_job_skills = random.randint(5, 10)
        job_skills = set(random.sample(SKILL_TAXONOMY, num_job_skills))
        
        # 2. Determine overlap based on target label
        if target_label == "Strong Match":
            # Match 90-100% of job skills
            overlap_count = int(len(job_skills) * random.uniform(0.9, 1.0))
        elif target_label == "Moderate Match":
            # Match 60-89% of job skills
            overlap_count = int(len(job_skills) * random.uniform(0.6, 0.89))
        elif target_label == "Skill Gap":
            # Match 30-59% of job skills
            overlap_count = int(len(job_skills) * random.uniform(0.3, 0.59))
        else: # High Skill Gap
            # Match 0-29% of job skills
            overlap_count = int(len(job_skills) * random.uniform(0.0, 0.29))
        
        # Ensure at least 0 overlap
        overlap_count = max(0, overlap_count)
        
        # 3. Construct Resume Skills
        # Start with the overlapping skills
        job_list = list(job_skills)
        random.shuffle(job_list)
        
        resume_skills = set(job_list[:overlap_count])
        
        # Add some random "noise" skills that the job didn't ask for
        other_skills = [s for s in SKILL_TAXONOMY if s not in job_skills]
        if other_skills:
            num_noise = random.randint(0, 3)
            resume_skills.update(random.sample(other_skills, min(num_noise, len(other_skills))))
            
        experience_years = random.randint(0, 15)
        
        return list(resume_skills), list(job_skills), experience_years

    # Generate data for each class
    for label in CLASS_LABELS:
        logger.info(f"Generating samples for class: {label}")
        for _ in range(n_samples_per_class):
            res_sk, job_sk, exp = create_sample(label)
            data.append({
                "resume_skills": ", ".join(sorted(res_sk)),
                "job_skills": ", ".join(sorted(job_sk)),
                "experience_years": exp,
                "label": label
            })
    
    # Shuffle data
    random.shuffle(data)
    
    df = pd.DataFrame(data)
    
    # Save
    processed_dir = os.path.join(DATA_DIR, "processed")
    os.makedirs(processed_dir, exist_ok=True)
    save_path = os.path.join(processed_dir, "training_data.csv")
    df.to_csv(save_path, index=False)
    
    logger.info(f"[SUCCESS] Data saved to: {save_path}")
    logger.info(f"Class Distribution:\n{df['label'].value_counts()}")
    return df

if __name__ == "__main__":
    generate_balanced_data(n_samples_per_class=350)