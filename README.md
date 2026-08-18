# Curriculum-Industry Skill Feature Store Using Feast

## Student Details
- **Name:** Hemanjaneyulu
- **Register Number:** `<YOUR_REGISTER_NUMBER>`
- **Section:** `<YOUR_SECTION>`
- **Required repository name:** `<RegisterNumber>MLOps-Feast-SkillGap`

> Replace the register number and section before submitting to GitHub.

## 1. Problem Statement
This project converts a curriculum-industry skill-gap dataset for 1,000 CSE students into a simple Feast feature store. The objective is to engineer reusable student-skill features, register them with Feast, retrieve historical features for model training, materialize them into an online SQLite store, retrieve online features, and use the same features in a machine-learning model to predict the **Skill_Gap_Index**.

The assignment requires demonstration of feature engineering, Feast entity/data source/FeatureView creation, `feast apply`, historical retrieval, materialization, online retrieval, ML usage, and GitHub documentation.

## 2. Dataset
- **Rows:** 1,000 students
- **Original columns:** 20
- **Domain specializations:** AI_ML, Cybersecurity, DataEngineering, DevOps, FullStack
- **Target:** `Skill_Gap_Index`
- **Entity:** `student_id` (derived from `Student_ID`)
- **How entries were created:** The supplied CSV is a synthetic/random student skill-gap dataset containing academic, technical, practical-experience, soft-skill, and industry-readiness variables.

### Original columns
`Student_ID`, `CGPA`, `DSA_Score`, `System_Design_Score`, `DBMS_Score`, `OOP_Proficiency`, `Cloud_DevOps_Score`, `Web_Dev_Score`, `Problem_Solving_Rating`, `Aptitude_Score`, `Communication_Rating`, `Teamwork_Score`, `Github_Projects_Count`, `Internship_Duration_Months`, `Certifications_Count`, `Hackathons_Participated`, `Mock_Interview_Score`, `Domain_Specialization`, `Curriculum_Updated_Year`, `Skill_Gap_Index`.

## 3. Data Cleaning
`src/prepare_data.py`:
1. Reads the supplied CSV.
2. Removes duplicate `Student_ID` values.
3. Converts numeric columns to numeric values.
4. Fills numeric missing values with the median.
5. Fills categorical missing values with the mode.
6. Creates `event_timestamp` for Feast.
7. Keeps `Skill_Gap_Index` outside the FeatureView to avoid target leakage.

## 4. Feature Engineering
The project creates reusable features:
- `cgpa`
- `dsa_score`
- `system_design_score`
- `dbms_score`
- `oop_proficiency`
- `cloud_devops_score`
- `web_dev_score`
- `problem_solving_score`
- `aptitude_score`
- `communication_score`
- `teamwork_score`
- `github_projects_count`
- `internship_duration_months`
- `certifications_count`
- `hackathons_participated`
- `mock_interview_score`
- `curriculum_updated_year`
- `domain_code`
- `technical_skill_mean`
- `soft_skill_mean`
- `industry_exposure_score`
- `practical_experience_score`
- `curriculum_age_years`

### Example feature calculation
`technical_skill_mean` is calculated as the mean of DSA, System Design, DBMS, OOP, Cloud/DevOps, and Web Development scores:

`technical_skill_mean = mean(DSA, System Design, DBMS, OOP, Cloud/DevOps, Web Development)`

`problem_solving_score` is normalized from the source scale by dividing `Problem_Solving_Rating` by 25. `communication_score` is converted from a 1–5 scale to approximately 0–100 by multiplying by 20.

## 5. Feast Architecture

```text
Original CSV Dataset
        |
        v
Data Cleaning + Feature Engineering
        |
        v
Parquet Offline Data + Labels
        |
        v
Feast FileSource
        |
        v
Feast FeatureView
        |
        +--------------------------+
        |                          |
        v                          v
Historical Retrieval         Materialization
        |                          |
        v                          v
Model Training               SQLite Online Store
                                   |
                                   v
                            Online Retrieval
                                   |
                                   v
                               Prediction
```

## 6. Feast Implementation

### Entity
The entity is `student_id`. It uniquely identifies one student and is used as the join key for feature retrieval.

### Data source
The Feast `FileSource` points to `data/processed/student_features.parquet`. The source contains `event_timestamp` so Feast can perform point-in-time historical retrieval.

### FeatureView
`student_skill_features` contains the reusable student academic, technical, soft-skill, practical-experience, and engineered features listed above. `Skill_Gap_Index` is deliberately not included as a feature because it is the prediction target.

### Historical retrieval
`src/get_historical.py` calls `get_historical_features()` using student IDs and timestamps. This produces the point-in-time feature set used by the model.

### Model
`src/train_model.py` trains a `RandomForestRegressor` to predict `Skill_Gap_Index`. The train/test split uses `random_state=42` and a 20% test set. Metrics are saved to `outputs/model_metrics.json`.

### Materialization
`src/materialize.py` calls Feast materialization for the available event-time range. This copies the latest feature values into the online SQLite store.

### Online retrieval
`src/get_online.py` calls `get_online_features()` for a student such as `CSE_0001`.

### Prediction
`src/predict.py` retrieves the same Feast feature vector online and sends it to the saved model.

## 7. Required Questions

### 1. What is the entity?
`student_id`, representing one student.

### 2. List the features stored in the FeatureView.
The FeatureView stores the 24 features listed in the Feature Engineering section.

### 3. Explain how one feature was calculated.
`technical_skill_mean` is the arithmetic mean of six technical skill scores: DSA, System Design, DBMS, OOP, Cloud/DevOps, and Web Development.

### 4. Difference between original dataset and feature dataset
The original dataset contains raw student attributes and the target. The feature dataset contains cleaned, model-ready numerical features, a Feast entity key, and an event timestamp. The target is kept separately for supervised learning and is not registered as an input feature.

### 5. Purpose of the offline store
The offline store keeps historical feature data and supports point-in-time retrieval for training and analysis.

### 6. Purpose of the online store
The online store keeps the latest feature values so applications can retrieve features quickly for prediction.

### 7. Purpose of `feast apply`
`feast apply` registers or updates the Feast entities, data sources, and FeatureViews in the feature repository.

### 8. What does materialization do?
Materialization loads feature values from the offline source into the online store for the specified time range.

### 9. Advantage of Feast over manually calculating features
The same centrally defined feature transformations can be reused for training and inference. This reduces duplicated feature logic and helps keep training and serving features consistent.

### 10. Two limitations of the current dataset
1. The dataset is synthetic/random and may not represent real hiring or curriculum evidence.
2. The dataset is a single snapshot rather than a rich longitudinal record of how a student's skills change over time.

### 11. Two improvements when more evidence is available
1. Add time-versioned curriculum outcomes, placement outcomes, job descriptions, interview results, and industry skill-demand evidence.
2. Add richer domain-specific features and production monitoring such as feature freshness, drift detection, data quality checks, and model performance tracking.

## 8. Run the Project

### Environment
Python 3.10/3.11 is recommended.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### Step 1: Prepare data
```bash
python src/prepare_data.py
```

### Step 2: Register Feast objects
```bash
cd feature_repo
feast apply
cd ..
```

### Step 3: Historical retrieval
```bash
python src/get_historical.py
```

### Step 4: Train model
```bash
python src/train_model.py
```

### Step 5: Materialize online store
```bash
python src/materialize.py
```

### Step 6: Online retrieval
```bash
python src/get_online.py
```

### Step 7: Final prediction
```bash
python src/predict.py
```

## 9. Expected Deliverables
- `data/processed/student_features.parquet`
- `data/processed/training_labels.parquet`
- Feast registry
- SQLite online store
- historical feature output
- trained model
- model metrics
- online feature output
- final prediction
- architecture diagram
- this README


## 9. Reference Results from the Supplied Dataset
A reference Random Forest run using the same engineered feature columns gives:
- **MAE:** 4.3342
- **RMSE:** 5.7924
- **R²:** 0.7827
- **Train/Test:** 800 / 200
- **Reference prediction for CSE_0001:** Skill_Gap_Index ≈ 8.30

These reference numbers are included so the repository has an immediate result. The formal Feast workflow should still be executed locally after installing Feast and PyArrow; the Feast-generated historical/online outputs may vary with the installed Feast version.

## 10. Submission
Create a GitHub repository named:

`<RegisterNumber>MLOps-Feast-SkillGap`

Push the complete project and submit the repository link through the faculty Google Form.
