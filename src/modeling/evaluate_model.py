import joblib
import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger

# 8
#ToRun:"python -m src.modeling.evaluate_model"

# -------------------------------------------------------
# SETUP LOGURU
# -------------------------------------------------------
# Remove the default handler to prevent duplicate logs
logger.remove()
# Add a new handler with a custom format and colors
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.config import DATA_DIR, MODEL_DIR, CLASS_LABELS
from src.features.feature_builder import FeatureEngineer

def evaluate():
    logger.info("[Phase 11] Starting Model Evaluation...")

    # 1. Load Data
    csv_path = os.path.join(DATA_DIR, "processed", "training_data.csv")
    df = pd.read_csv(csv_path)
    
    # Handle missing values
    df['resume_skills'] = df['resume_skills'].fillna("")
    df['job_skills'] = df['job_skills'].fillna("")
    
    # Convert strings back to lists
    resume_lists = [s.split(", ") if s else [] for s in df['resume_skills']]
    job_lists = [s.split(", ") if s else [] for s in df['job_skills']]
    
    # Encode Labels
    label_map = {label: i for i, label in enumerate(CLASS_LABELS)}
    y = df['label'].map(label_map)
    
    # 2. SPLIT DATA (Critical Step!)
    # We must split exactly the same way as train.py to get the TEST set
    logger.info("[Phase 11] Splitting data to isolate Test Set...")
    res_train, res_test, job_train, job_test, y_train, y_test = train_test_split(
        resume_lists, job_lists, y, 
        test_size=0.2, random_state=42, stratify=y
    )
    
    # 3. Load Artifacts
    model = joblib.load(os.path.join(MODEL_DIR, "skill_gap_model.joblib"))
    fe = joblib.load(os.path.join(MODEL_DIR, "feature_engineer.joblib"))
    
    # 4. Feature Engineering
    # We only transform the TEST set for evaluation
    # Note: We don't need to fit again, the loaded 'fe' is already fitted
    X_test = fe.transform(res_test, job_test)
    
    # 5. Predict
    preds = model.predict(X_test)
    
    # 6. Print Classification Report
    logger.info("--- Classification Report (Test Set) ---")
    report = classification_report(y_test, preds, target_names=CLASS_LABELS)
    # Print report to logs (handling newlines)
    for line in report.split('\n'):
        logger.info(line)
    
    # 7. Plot Confusion Matrix
    logger.info("[Phase 11] Generating Confusion Matrix...")
    cm = confusion_matrix(y_test, preds)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=CLASS_LABELS, yticklabels=CLASS_LABELS)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix (Test Set)')
    
    # Save plot
    eval_path = os.path.join(MODEL_DIR, "confusion_matrix.png")
    plt.savefig(eval_path)
    
    # Optional: Comment this out if you don't want a window popping up
    # plt.show() 
    
    logger.info(f"[SUCCESS] Confusion Matrix saved to: {eval_path}")

if __name__ == "__main__":
    evaluate()