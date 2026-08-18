from pathlib import Path
import sys
import numpy as np
import pandas as pd
import joblib

ROOT = Path(__file__).resolve().parents[1]
FEATURE_REPO = ROOT / "feature_repo"
sys.path.insert(0, str(FEATURE_REPO))

from feast import FeatureStore

def main(student_id="CSE_0001"):
    store = FeatureStore(repo_path=str(FEATURE_REPO))
    bundle = joblib.load(ROOT / "models/skill_gap_model.joblib")
    model = bundle["model"]
    feature_names = bundle["feature_names"]

    feature_refs = [f"student_skill_features:{name}" for name in feature_names]

    raw = store.get_online_features(
        features=feature_refs,
        entity_rows=[{"student_id": student_id}],
    ).to_dict()

    X = pd.DataFrame(raw)
    X = X.reindex(columns=feature_names)

    prediction = float(model.predict(X)[0])
    print(f"Student: {student_id}")
    print(f"Predicted Skill_Gap_Index: {prediction:.2f}")

    (ROOT / "outputs/final_prediction.txt").write_text(
        f"Student: {student_id}\nPredicted Skill_Gap_Index: {prediction:.2f}\n"
    )

if __name__ == "__main__":
    main()
