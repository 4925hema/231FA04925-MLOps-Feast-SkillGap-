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
    start = pd.to_datetime(labels["event_timestamp"].min()).to_pydatetime()
    end = (pd.to_datetime(labels["event_timestamp"].max()) + pd.Timedelta(days=1)).to_pydatetime()

    # The source is a snapshot. Use an exclusive end boundary one day after the event date.
    store.materialize(start_date=start, end_date=end)
    print("Materialization completed.")
    print("Online store:", FEATURE_REPO / "data/online_store.db")

if __name__ == "__main__":
    main()
