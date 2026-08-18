from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def test_processed_files_exist():
    assert (ROOT / "data/processed/student_features.parquet").exists()
    assert (ROOT / "data/processed/training_labels.parquet").exists()

def test_no_target_leakage():
    features = pd.read_parquet(ROOT / "data/processed/student_features.parquet")
    assert "skill_gap_index" not in features.columns
    assert "Skill_Gap_Index" not in features.columns
