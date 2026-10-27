import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import os
import sys
import joblib
import mlflow
import mlflow.sklearn
import pathlib
from loguru import logger

# 6 & 7
#ToRun:"python -m src.modeling.train"
#Next :"mlflow ui"
#If you want to run again 
#then delete "mlruns" folder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score

# -------------------------------------------------------
# SETUP LOGURU
# -------------------------------------------------------
# Remove the default handler to prevent duplicate logs
logger.remove()
# Add a new handler with a custom format and colors
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}")

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.config import BASE_DIR, DATA_DIR, MODEL_DIR, CLASS_LABELS
from src.features.feature_builder import FeatureEngineer

def train():
    logger.info("[Phase 10] Starting High-Accuracy Pipeline...")

    # MLFLOW SETUP
    mlruns_path = os.path.join(BASE_DIR, "mlruns")
    tracking_uri = pathlib.Path(mlruns_path).as_uri()
    mlflow.set_tracking_uri(tracking_uri)

    # 1. Load Data
    csv_path = os.path.join(DATA_DIR, "processed", "training_data.csv")
    df = pd.read_csv(csv_path)
    
    df['resume_skills'] = df['resume_skills'].fillna("")
    df['job_skills'] = df['job_skills'].fillna("")
    
    resume_lists = [s.split(", ") if s else [] for s in df['resume_skills']]
    job_lists = [s.split(", ") if s else [] for s in df['job_skills']]
    
    label_map = {label: i for i, label in enumerate(CLASS_LABELS)}
    y = df['label'].map(label_map)
    
    # Split Data
    logger.info("[Phase 10] Splitting Data...")
    res_train, res_test, job_train, job_test, y_train, y_test = train_test_split(
        resume_lists, job_lists, y, 
        test_size=0.2, random_state=42, stratify=y
    )
    
    # Feature Engineering
    fe = FeatureEngineer()
    fe.fit(res_train, job_train)
    X_train = fe.transform(res_train, job_train)
    X_test = fe.transform(res_test, job_test)

    # EXPERIMENT
    mlflow.set_experiment("Skill_Gap_High_Accuracy")

    with mlflow.start_run():
        
        # 1. Use Gradient Boosting (Usually higher accuracy)
        model = GradientBoostingClassifier(random_state=42)
        
        param_grid = {
            'n_estimators': [100, 200],
            'learning_rate': [0.05, 0.1],
            'max_depth': [3, 5, 7],
            'min_samples_split': [2, 5]
        }
        
        logger.info("[Phase 10] Tuning Model (GradientBoosting)...")

        grid_search = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=5,
            scoring='accuracy', # Maximize accuracy directly
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        best_model = grid_search.best_estimator_
        best_params = grid_search.best_params_
        
        logger.info(f"Best Parameters Found: {best_params}")
        mlflow.log_param("best_params", best_params)
        
        # Evaluate
        preds = best_model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        
        mlflow.log_metric("accuracy", acc)
        logger.info(f"[Phase 10] Logged Metric: Accuracy = {acc:.4f}")
        
        # Log classification report
        report = classification_report(y_test, preds, output_dict=True, target_names=CLASS_LABELS)
        for label, metrics in report.items():
            if isinstance(metrics, dict):
                for metric_name, value in metrics.items():
                    mlflow.log_metric(f"{label}_{metric_name}", value)
        
        # Log Model
        mlflow.sklearn.log_model(best_model, "gradient_boost_model", registered_model_name="SkillGapClassifier")
        
        # Save Artifacts
        joblib.dump(best_model, os.path.join(MODEL_DIR, "skill_gap_model.joblib"))
        joblib.dump(fe, os.path.join(MODEL_DIR, "feature_engineer.joblib"))
        
        logger.info(f"[SUCCESS] Training Complete. Accuracy: {acc:.4f}")

if __name__ == "__main__":
    train()