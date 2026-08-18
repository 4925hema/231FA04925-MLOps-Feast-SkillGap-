from pathlib import Path
import sys
import json

ROOT = Path(__file__).resolve().parents[1]
FEATURE_REPO = ROOT / "feature_repo"
sys.path.insert(0, str(FEATURE_REPO))

from feast import FeatureStore

def main():
    store = FeatureStore(repo_path=str(FEATURE_REPO))

    entity_rows = [{"student_id": "CSE_0001"}]
    feature_refs = [
        "student_skill_features:cgpa",
        "student_skill_features:dsa_score",
        "student_skill_features:technical_skill_mean",
        "student_skill_features:industry_exposure_score",
        "student_skill_features:practical_experience_score",
        "student_skill_features:mock_interview_score",
    ]

    response = store.get_online_features(
        features=feature_refs,
        entity_rows=entity_rows,
    ).to_dict()

    (ROOT / "outputs/online_features.json").write_text(
        json.dumps(response, indent=2, default=str)
    )
    print(json.dumps(response, indent=2, default=str))

if __name__ == "__main__":
    main()
