# Windows setup

1. Install Python 3.10 or 3.11.
2. Open Command Prompt in the project folder.
3. Create the environment:
```bat
python -m venv .venv
.venv\Scripts\activate
```
4. Install dependencies:
```bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```
5. Generate Parquet feature data:
```bat
python src\prepare_data.py
```
6. Register Feast:
```bat
cd feature_repo
feast apply
cd ..
```
7. Run the complete flow:
```bat
python run_project.py
```

If `feast` is not recognized, run:
```bat
python -m feast apply
```
