from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FEATURE_REPO = ROOT / "feature_repo"
sys.path.insert(0, str(FEATURE_REPO))

from feast import FeatureStore

def main():
    store = FeatureStore(repo_path=str(FEATURE_REPO))
    labels = pd.read_parquet(ROOT / "data/processed/training_labels.parquet")

    entity_df = labels[["student_id", "event_timestamp"]].copy()

    feature_refs = [
        "student_skill_features:cgpa",
        "student_skill_features:dsa_score",
        "student_skill_features:technical_skill_mean",
        "student_skill_features:industry_exposure_score",
        "student_skill_features:practical_experience_score",
        "student_skill_features:curriculum_age_years",
        "student_skill_features:mock_interview_score",
    ]

    historical = store.get_historical_features(
        entity_df=entity_df,
        features=feature_refs,
    ).to_df()

    historical.to_csv(ROOT / "outputs/historical_features.csv", index=False)
    print(historical.head(10).to_string(index=False))
    print(f"\nSaved {len(historical)} rows to outputs/historical_features.csv")

if __name__ == "__main__":
    main()
