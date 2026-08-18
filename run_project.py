from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def run(cmd, cwd=None):
    print("\n>>>", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)

def main():
    run([sys.executable, "src/prepare_data.py"])
    run(["feast", "apply"], cwd=ROOT / "feature_repo")
    run([sys.executable, "src/get_historical.py"])
    run([sys.executable, "src/train_model.py"])
    run([sys.executable, "src/materialize.py"])
    run([sys.executable, "src/get_online.py"])
    run([sys.executable, "src/predict.py"])
    print("\nPROJECT COMPLETED.")

if __name__ == "__main__":
    main()
