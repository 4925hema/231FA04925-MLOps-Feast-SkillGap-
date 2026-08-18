from pathlib import Path
import sys
import json
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
FEATURE_REPO = ROOT / "feature_repo"
sys.path.insert(0, str(FEATURE_REPO))

from feast import FeatureStore

MODEL_DIR = ROOT / "models"
OUT_DIR = ROOT / "outputs"
MODEL_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

def main():
    store = FeatureStore(repo_path=str(FEATURE_REPO))
    labels = pd.read_parquet(ROOT / "data/processed/training_labels.parquet")
    entity_df = labels[["student_id", "event_timestamp"]]

    feature_refs = [
        f"student_skill_features:{name}" for name in [
            "cgpa", "dsa_score", "system_design_score", "dbms_score",
            "oop_proficiency", "cloud_devops_score", "web_dev_score",
            "problem_solving_score", "aptitude_score", "communication_score",
            "teamwork_score", "github_projects_count",
            "internship_duration_months", "certifications_count",
            "hackathons_participated", "mock_interview_score",
            "curriculum_updated_year", "domain_code", "technical_skill_mean",
            "soft_skill_mean", "industry_exposure_score",
            "practical_experience_score", "curriculum_age_years"
        ]
    ]

    X = store.get_historical_features(
        entity_df=entity_df,
        features=feature_refs
    ).to_df()

    y = labels["skill_gap_index"].reset_index(drop=True)
    X = X.drop(columns=["event_timestamp", "student_id"], errors="ignore").reset_index(drop=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        max_depth=12,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    metrics = {
        "model": "RandomForestRegressor",
        "target": "Skill_Gap_Index",
        "train_rows": len(X_train),
        "test_rows": len(X_test),
        "mae": float(mean_absolute_error(y_test, pred)),
        "rmse": float(mean_squared_error(y_test, pred) ** 0.5),
        "r2": float(r2_score(y_test, pred)),
    }

    joblib.dump(
        {"model": model, "feature_names": list(X.columns)},
        MODEL_DIR / "skill_gap_model.joblib"
    )
    (OUT_DIR / "model_metrics.json").write_text(json.dumps(metrics, indent=2))

    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    main()
